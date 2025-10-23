
# Security Notes

- Use TLS and authenticate servers (mTLS or signed tokens).
- Pad and batch requests to fixed sizes to reduce traffic analysis.
- Store server endpoints in a trusted configuration; rotate keys regularly if using masked shares with PRGs.
- Consider rate limits and replay protection.
- Engage a professional security review before production use.
