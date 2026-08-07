# DNS cutover: Squarespace → GitHub Pages

## ✅ Completed 7 August 2026

www.chesdata.eu now serves from GitHub Pages over HTTPS. Kept as a record of
what changed and how to undo it.

| Check | Result |
|---|---|
| Apex `A` records → GitHub | ✅ |
| `www` `CNAME` → `chesdata.github.io` | ✅ |
| Propagation (Google, Cloudflare, Quad9) | ✅ |
| All ten pages + redirect stubs + assets | ✅ `200` |
| TLS certificate for `www.chesdata.eu` | ✅ issued 22:05 UTC, auto-renews |
| TLS certificate for bare `chesdata.eu` | ✅ |
| Enforce HTTPS | ✅ on |
| `http://` and bare-domain redirects | ✅ all land on `https://www.chesdata.eu` |
| Mail records | ✅ untouched |

**Squarespace was still live at the time of writing.** Leave it a week or two
before cancelling; the rollback values below stop being useful once it's gone.

Every value below was read off live DNS and off GitHub's own documentation on
**7 August 2026**. Re-check the GitHub IPs against the docs link at the bottom
if you are reading this much later — they have changed before.

---

## The mail records: left alone, and unused anyway

The zone carries a **Microsoft 365 mail setup** plus Teams/Skype service
records. It was left completely untouched by the cutover, which is the right
default — but it turns out CHES doesn't use it. The working address is a
plain Gmail account (`chesdata@gmail.com`, set in `_config.yml`), and no mail
is read at any `@chesdata.eu` address.

The `NETORGFT…onmicrosoft.com` verification record is the signature of a
Microsoft 365 tenant auto-provisioned by GoDaddy at registration, so this is
almost certainly a bundled extra nobody ever set up. It can be deleted from the
GoDaddy zone whenever someone feels like tidying, or left indefinitely — it
costs nothing and breaks nothing. If you do delete it, take the whole set
together, and be aware that anything ever sent to an `@chesdata.eu` address
will then bounce rather than vanish silently into the unread tenant.

The records, for reference:

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

*(Not done in the event — the change went cleanly and propagated fast.)*

The `www` record has a **1-hour TTL**, so a mistake takes up to an hour to undo.
If you can wait, set the TTL on the apex `A` records and the `www` `CNAME` to
**600 seconds**, leave it an hour, *then* make the changes above. Rollback then
costs ten minutes instead of sixty. Put the TTLs back up once you're happy.

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

## After the change — all done, kept for reference

1. **Wait** for propagation. In the event it went to all three public resolvers
   within minutes, not the hour the TTL allowed for. Check with:
   ```
   dig +short www.chesdata.eu
   ```
   You want `chesdata.github.io` and the `185.199.x.153` addresses.
2. **GitHub → Settings → Pages.** The custom domain was already set to
   `www.chesdata.eu` (the repo's `CNAME` file does this) and the DNS check
   went green immediately.
3. **Tick "Enforce HTTPS"** once the tick appears — not before. The green DNS
   tick is what makes GitHub request the certificate, so "Enforce HTTPS" being
   greyed out straight afterwards is expected, not a fault; it became tickable
   within the hour. There are no `CAA` records on the domain, so nothing blocked
   issuance. GitHub issued two certificates, one for `www.chesdata.eu` and one
   for the bare `chesdata.eu`, and renews both automatically.
4. **Check the site over HTTPS.** Done — all ten pages, the three redirect
   stubs, and the static assets return `200`, and all four entry points
   (`http`/`https` × bare/`www`) land on `https://www.chesdata.eu`.
5. **Leave Squarespace running for a week or two.** Cancel only once you've
   stopped needing the rollback values above.

One gotcha during the changeover: your own machine caches the old record for up
to the TTL, so the site can look unchanged locally long after it has switched
for everyone else. Compare `dig +short www.chesdata.eu` against
`dig @1.1.1.1 +short www.chesdata.eu` to tell the two apart, and flush with
`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.

---

## Why chesdata.github.io didn't work as a preview URL

Once the `CNAME` file is committed, GitHub Pages answers
`https://chesdata.github.io/` with a `301` to `www.chesdata.eu`. Before the
cutover that was still Squarespace, so the test site bounced to the old site
and the README's "look at the test site first" step didn't work as written.

The way round it, useful any time you need to see what a host is serving before
DNS points at it, is to force the resolve:

```
curl --resolve www.chesdata.eu:80:185.199.108.153 http://www.chesdata.eu/
```

All ten pages, the three redirect stubs, the stylesheet, the logo, the sitemap,
and the favicon returned `200`. If you want to browse it properly before the
cutover, either run `python3 build-preview.py` locally, or temporarily remove
the `CNAME` file, push, look at `chesdata.github.io`, then put it back.

---

# Zone cleanup

Full inventory taken 7 August 2026 after the cutover. The zone had accumulated
sixteen records; five of them do anything.

## Never touch: the `NS` and `SOA` records

```
chesdata.eu.  3600  IN  NS   ns17.domaincontrol.com.
chesdata.eu.  3600  IN  NS   ns18.domaincontrol.com.
chesdata.eu.   600  IN  SOA  ns17.domaincontrol.com. dns.jomax.net. 2026080707 28800 7200 604800 600
```

The `SOA` is what makes the zone a zone: every zone has exactly one, at the
apex, and GoDaddy creates and maintains it automatically. It names which of the
two nameservers holds the master copy, GoDaddy's own admin address
(`dns@jomax.net` — the first dot stands in for the `@`), a serial number that
bumps on every save so the replica knows to re-sync, and GoDaddy's internal
replication intervals. The only field with any visible effect is the last, the
600-second negative TTL, which is how long resolvers remember that a record you
deleted is gone. It cannot be deleted and there is no reason to edit it.

These are not service records that went stale with Squarespace — they are the
delegation itself, the `.eu` registry's statement of which servers may answer
for this domain. Every lookup starts there. Remove or mistype them and the
domain stops resolving worldwide until it's fixed and the TTL expires.

GoDaddy shows them in the record list but won't let you edit them there;
nameservers change through a separate control on the domain settings page.
Skip past them. The only reason to touch them is moving DNS hosting to another
provider entirely, which is a migration, not a cleanup.

DNSSEC is off (no `DS` record at the registry). That's normal and fine. Turning
it on protects against DNS spoofing, but a botched rollout is a common way to
lose a domain for a day, and the payoff for a public static site with no login
and no mail is thin. Recommend leaving it off.

## Keep

| Type | Name | Value | Why |
|---|---|---|---|
| A ×4 | `@` | `185.199.108–111.153` | the site |
| CNAME | `www` | `chesdata.github.io` | the site |
| CNAME | `_domainconnect` | `_domainconnect.gd.domaincontrol.com` | GoDaddy plumbing; harmless |

## Delete: dead Microsoft 365

Auto-provisioned by GoDaddy at registration and never used — CHES mail is a
plain Gmail account. Check the `MX` question below before removing these.

```
MX     @                        chesdata-eu.mail.protection.outlook.com
TXT    @                        NETORGFT10890541.onmicrosoft.com
CNAME  autodiscover             autodiscover.outlook.com
CNAME  lyncdiscover             webdir.online.lync.com
CNAME  sip                      sipdir.online.lync.com
CNAME  msoid                    clientconfig.microsoftonline-p.net
SRV    _sip._tls                sipdir.online.lync.com:443
SRV    _sipfederationtls._tcp   sipfed.online.lync.com:5061
```

## Delete: dead GoDaddy defaults

```
CNAME  email   email.secureserver.net      GoDaddy webmail, unused
CNAME  ftp     chesdata.eu                 now points at Pages, which has no FTP
```

## Delete only after Squarespace is cancelled

Squarespace's domain-verification pair — one token planted twice. No traffic
passes through either; they're proof of ownership. While the subscription is
live they're what keeps Squarespace recognising the domain, which the rollback
path depends on.

```
CNAME  ayewrgn3m3dm2lgzmz3z   verify.squarespace.com.
TXT    @                      "ayewrgn3m3dm2lgzmz3z"
```

## Check before deleting the `MX` record

DNS can show that mail for the domain routes to a Microsoft 365 tenant. It
cannot show whether that tenant forwards to the Gmail account. Send a test
message to `info@chesdata.eu`:

- **Bounces or vanishes** — nothing is there, delete freely.
- **Arrives in Gmail** — a forward is live. Keep the `MX` and its supporting
  `TXT` records, and turn the forward off at Microsoft before removing anything.

As it stands, mail to the domain most likely lands in a mailbox nobody reads and
the sender never finds out. Removing the `MX` is an improvement either way —
senders get an immediate bounce instead of silence.

## Add: stop the domain being spoofed

The domain sends no mail, which currently means anyone can forge
`From: someone@chesdata.eu` and nothing contradicts them.

```
TXT  @        v=spf1 -all                                          (replaces the include:secureserver.net one)
TXT  _dmarc   v=DMARC1; p=reject; rua=mailto:chesdata@gmail.com
```

Together these say the domain never sends mail and anything claiming otherwise
should be rejected. Cheap insurance for a project whose name carries academic
weight.

## End state

The `SOA`, two `NS`, four `A`, `www`, `_domainconnect`, and the two
anti-spoofing `TXT` records. Eleven records instead of seventeen, and every one
of them doing something.

---

GitHub's current IP addresses, should you need to re-verify:
<https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>
