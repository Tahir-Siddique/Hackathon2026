# CVE-to-My-Stack — Executive Brief

## Summary
- **Assets mapped:** 12
- **Assets unmapped:** 0
- **Prioritised CVEs shown:** 50
- **KEV (actively exploited) in list:** 13

## Mapped stack

- Microsoft 365 Apps for Business Current → `microsoft:365_apps`
- Windows Server 2022 21H2 → `microsoft:windows_server_2022`
- Windows 10 Pro 22H2 → `microsoft:windows_10`
- Adobe Acrobat Reader DC 2024.001 → `adobe:acrobat_reader`
- Cisco IOS XE 17.9 → `cisco:ios_xe`
- VMware vSphere 8.0 → `vmware:vsphere`
- Google Chrome Latest → `google:chrome`
- OpenSSL 3.0.7 → `openssl:openssl`
- Apache HTTP Server 2.4.57 → `apache:http_server`
- Zoom 5.17 → `zoom:zoom`
- WordPress 6.4 → `wordpress:wordpress`
- Moodle 4.3 → `moodle:moodle`

## Top priorities

1. **CVE-2026-32202** — Windows Server 2022 21H2 (CVSS 4.3, EPSS 0.5682, KEV yes)
   - CVE-2026-32202 affects Windows Server 2022 21H2. EPSS 0.5682 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
2. **CVE-2026-21513** — Windows Server 2022 21H2 (CVSS 8.8, EPSS 0.2496, KEV yes)
   - CVE-2026-21513 affects Windows Server 2022 21H2. EPSS 0.2496 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
3. **CVE-2026-2441** — Google Chrome Latest (CVSS 8.8, EPSS 0.2313, KEV yes)
   - CVE-2026-2441 affects Google Chrome Latest. EPSS 0.2313 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
4. **CVE-2026-21533** — Windows Server 2022 21H2 (CVSS 7.8, EPSS 0.2020, KEV yes)
   - CVE-2026-21533 affects Windows Server 2022 21H2. EPSS 0.2020 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
5. **CVE-2026-21509** — Microsoft 365 Apps for Business Current (CVSS 7.8, EPSS 0.1387, KEV yes)
   - CVE-2026-21509 affects Microsoft 365 Apps for Business Current. EPSS 0.1387 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
6. **CVE-2026-21510** — Windows Server 2022 21H2 (CVSS 8.8, EPSS 0.0496, KEV yes)
   - CVE-2026-21510 affects Windows Server 2022 21H2. EPSS 0.0496 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
7. **CVE-2026-3910** — Google Chrome Latest (CVSS 8.8, EPSS 0.0324, KEV yes)
   - CVE-2026-3910 affects Google Chrome Latest. EPSS 0.0324 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
8. **CVE-2026-5281** — Google Chrome Latest (CVSS 8.8, EPSS 0.0065, KEV yes)
   - CVE-2026-5281 affects Google Chrome Latest. EPSS 0.0065 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
9. **CVE-2026-3909** — Google Chrome Latest (CVSS 8.8, EPSS 0.0045, KEV yes)
   - CVE-2026-3909 affects Google Chrome Latest. EPSS 0.0045 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
10. **CVE-2026-21514** — Microsoft 365 Apps for Business Current (CVSS 7.8, EPSS 0.0517, KEV yes)
   - CVE-2026-21514 affects Microsoft 365 Apps for Business Current. EPSS 0.0517 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).

## Limitations
- Wrong product mapping → CVE may be missing silently.
- EPSS is predictive, not proof of safety.
- Not in KEV ≠ unexploited.
- Version ranges are not matched in this MVP.
