# DNS cutover: Squarespace → GitHub Pages

Every value below was read off live DNS and off GitHub's own documentation on
**7 August 2026**. Re-check the GitHub IPs against the docs link at the bottom
if you are reading this much later — they have changed before.

---

## ⚠️ Read this first: chesdata.eu runs email

The domain is not just a website. It carries a working **Microsoft 365 mail
setup**, plus Teams/Skype service records:

| Record | Host | Value |
|---|---|---|
| MX | `@` | `chesdata-eu.mail.protection.outlook.com` (priority 0) |
| TXT | `@` | `v=spf1 include:secureserver.net -all` |
| TXT | `@` | `NETORGFT10890541.onmicrosoft.com` |
| TXT | `@` | `ayewrgn3m3dm2lgzmz3z` |
| CNAME | `autodiscover` | `autodiscover.outlook.com` |
| CNAME | `lyncdiscover` | `webdir.online.lync.com` |
| CNAME | `sip` | `sipdir.online.lync.com` |
| CNAME | `msoid` | `clientconfig.microsoftonline-p.net` |
| SRV | `_sip._tls` | `sipdir.online.lync.com:443` |
| SRV | `_sipfederationtls._tcp` | `sipfed.online.lync.com:5061` |

**Do not delete these.** The cutover touches exactly two things: the four apex
`A` records and the `www` `CNAME`. Nothing else. If you find yourself using a
"remove all Squarespace records" button, stop — it will take the mail with it.

---

## Where the DNS actually lives

**GoDaddy.** This was an open question in the README; it is now settled. The
nameservers for chesdata.eu are `ns17.domaincontrol.com` and
`ns18.domaincontrol.com`, which are GoDaddy's. Squarespace hosts the *site* but
does not control the *DNS*, so every record change below happens in the GoDaddy
DNS panel and nothing needs to be done inside Squarespace.

---

## The changes

In GoDaddy: **My Products → chesdata.eu → DNS → Manage Zones**.

### 1. Replace the four apex `A` records

| Host | Current value (Squarespace) | New value (GitHub) |
|---|---|---|
| `@` | `198.185.159.144` | `185.199.108.153` |
| `@` | `198.185.159.145` | `185.199.109.153` |
| `@` | `198.49.23.144`   | `185.199.110.153` |
| `@` | `198.49.23.145`   | `185.199.111.153` |

These exist so the bare `chesdata.eu` works. Once they point at GitHub, GitHub
redirects the bare domain to `www.chesdata.eu` automatically.

### 2. Repoint the `www` `CNAME`

| Host | Current value | New value |
|---|---|---|
| `www` | `ext-cust.squarespace.com` | `chesdata.github.io` |

Note the target is the **repository's** `github.io` host, not the custom domain.

### 3. Optional: add IPv6

Not required, and skip it if the GoDaddy UI makes it awkward. Four `AAAA`
records on `@`:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

---

## Optional but recommended: lower the TTLs first

The `www` record currently has a **1-hour TTL**, so a mistake takes up to an
hour to undo. If you can wait, set the TTL on the apex `A` records and the
`www` `CNAME` to **600 seconds**, leave it an hour, *then* make the changes
above. Rollback then costs ten minutes instead of sixty. Put the TTLs back up
once you're happy.

---

## Rollback values

Captured from live DNS before any change. To go back to Squarespace, restore:

```
A     @     198.185.159.144
A     @     198.185.159.145
A     @     198.49.23.144
A     @     198.49.23.145
CNAME www   ext-cust.squarespace.com
```

Keep the Squarespace subscription paid until you've stopped needing this list.

---

## After the change

1. **Wait.** Up to an hour at the current TTL. Check progress with:
   ```
   dig +short www.chesdata.eu
   ```
   You want `chesdata.github.io` and the `185.199.x.153` addresses, not
   `ext-cust.squarespace.com`.
2. **GitHub → Settings → Pages.** The custom domain is already set to
   `www.chesdata.eu` (the repo's `CNAME` file does this). The DNS check there
   should flip to a green tick.
3. **Tick "Enforce HTTPS"** once the tick appears — not before. The certificate
   is issued automatically by Let's Encrypt and is free. It can take a few
   minutes to an hour after DNS resolves. There are no `CAA` records on the
   domain, so nothing is blocking issuance.
4. **Check the site over HTTPS**, including a hard refresh, and click through
   the nav.
5. **Send a test email** to an address on the domain, and reply from it. This is
   the check that matters most — do it even though the mail records were left
   alone.
6. **Leave Squarespace running for a week or two.** Cancel only once mail and
   site have both been fine for a while.

---

## Why you can't preview at chesdata.github.io right now

Because the `CNAME` file is committed, GitHub Pages answers
`https://chesdata.github.io/` with a `301` to `http://www.chesdata.eu/` — which
is still Squarespace. So the test site currently bounces to the old site, and
the README's "look at the test site first" step no longer works as written.

The deployed build is fine — it was verified on 7 August 2026 by forcing a
local resolve past DNS:

```
curl --resolve www.chesdata.eu:80:185.199.108.153 http://www.chesdata.eu/
```

All ten pages, the three redirect stubs, the stylesheet, the logo, the sitemap,
and the favicon returned `200`. If you want to browse it properly before the
cutover, either run `python3 build-preview.py` locally, or temporarily remove
the `CNAME` file, push, look at `chesdata.github.io`, then put it back.

---

GitHub's current IP addresses, should you need to re-verify:
<https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>
