from ecdsa import SigningKey, NIST521p
sk = SigningKey.generate(curve=NIST521p)
vk = sk.verifying_key
with open("private.pem", "wb") as f:
    f.write(sk.to_pem())
with open("public.pem", "wb") as f:
    f.write(vk.to_pem())

with open("private.pem") as f:
    sk = SigningKey.from_pem(f.read())
with open("message.txt", "rb") as f:
    message = f.read()
sig = sk.sign(message)
with open("signature", "wb") as f:
    f.write(sig)

