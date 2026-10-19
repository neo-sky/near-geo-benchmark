import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score

API = "https://1click.chaindefuser.com/v0"
HEADERS = {"Content-Type": "application/json", "User-Agent": "near-geo-quote-check/1.0"}
QUOTE_CODE = re.compile(r"/v0/quote|getQuote|originAsset")
SDK = re.compile(r"1click\.chaindefuser\.com|OneClickService|one-click-sdk")
LITERAL = (r"""("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`[^`$]*`"""
           r"""|-?\d+(?:\.\d+)?|true|false|True|False)""")
SWAP_TYPE_NAME = re.compile(r"\bswapType\b[\"']?\s*[:=]\s*[\w.]*?"
                            r"\b(EXACT_INPUT|EXACT_OUTPUT|FLEX_INPUT|ANY_INPUT)\b")
EVM_CHAINS = {"eth", "base", "arb", "op", "pol", "bsc", "avax", "gnosis", "bera", "abs", "monad",
              "plasma", "scroll", "xlayer", "hood"}
BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58(raw):
    number, text = int.from_bytes(raw, "big"), ""
    while number:
        number, digit = divmod(number, 58)
        text = BASE58[digit] + text
    return text


DUMMY = {"sol": base58(bytes([2] * 32)), "near": "02" * 32}
EVM_DUMMY = "0x" + "02" * 20


def tokens():
    request = urllib.request.Request(f"{API}/tokens", headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as res:
        return {t["assetId"]: t["blockchain"] for t in json.load(res)}


def literal(code, field):
    match = re.search(rf"\b{field}\b[\"']?\s*[:=]\s*{LITERAL}", code)
    if not match:
        return None
    value = match.group(1)
    if value[0] in "\"'`":
        return value[1:-1]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def dummy(chain):
    return EVM_DUMMY if chain in EVM_CHAINS else DUMMY.get(chain)


def replay(body, cache):
    key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
    if key in cache:
        return cache[key]
    request = urllib.request.Request(f"{API}/quote", data=json.dumps(body).encode(),
                                     headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as res:
            outcome = {"status": res.status, "ok": True, "message": ""}
    except urllib.error.HTTPError as err:
        outcome = {"status": err.code, "ok": False, "message": err.read().decode()[:200]}
    except (urllib.error.URLError, TimeoutError) as err:
        outcome = {"status": 0, "ok": False, "message": str(err)[:200]}
    cache[key] = outcome
    time.sleep(0.5)
    return outcome


def swap_type(code):
    value = literal(code, "swapType")
    if value:
        return value
    match = SWAP_TYPE_NAME.search(code)
    return match.group(1) if match else None


def check(code, assets, cache):
    fields = {f: literal(code, f) for f in score.QUOTE_REQUIRED}
    fields["swapType"] = swap_type(code)
    present = sum(bool(re.search(rf"\b{f}\b[\"']?\s*[:=]", code)) for f in score.QUOTE_REQUIRED)
    origin, destination = fields["originAsset"], fields["destinationAsset"]
    known = all(a in assets for a in (origin, destination)) if origin and destination else None
    result = {
        "host_or_sdk": bool(SDK.search(code)),
        "fields_present": present,
        "swap_type_valid": fields["swapType"] in score.SWAP_TYPES if fields["swapType"] else None,
        "assets_known": known,
        "replay": None,
    }
    amount = fields["amount"]
    if not (known and result["swap_type_valid"] and amount and str(amount).isdigit()):
        return result
    refund, recipient = dummy(assets[origin]), dummy(assets[destination])
    if not refund or not recipient:
        return result
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    body = {"dry": True, "swapType": fields["swapType"],
            "slippageTolerance": int(fields["slippageTolerance"] or 100),
            "originAsset": origin, "depositType": "ORIGIN_CHAIN", "destinationAsset": destination,
            "amount": str(amount), "refundTo": refund, "refundType": "ORIGIN_CHAIN",
            "recipient": recipient, "recipientType": "DESTINATION_CHAIN",
            "deadline": expiry.strftime("%Y-%m-%dT%H:%M:%S.000Z")}
    result["replay"] = replay(body, cache)
    return result


def main():
    arms, out = sys.argv[1].split(","), Path(sys.argv[2])
    assets, cache, rows = tokens(), {}, []
    for arm in arms:
        for path in sorted((score.E / "runs" / arm).glob("*.json*")):
            if path.name.startswith("canary") or path.name.endswith(".tmp"):
                continue
            run = score.read_run(arm, path)
            if run["error"]:
                continue
            blocks = [b for b in score.CODE.findall(run["text"]) if QUOTE_CODE.search(b)]
            if blocks:
                outcome = check("\n".join(blocks), assets, cache)
                rows.append({"arm": arm, "file": path.name, **outcome})
    out.write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} answers with quote code, {sum(1 for r in rows if r['replay'])} replayed")


if __name__ == "__main__":
    main()
