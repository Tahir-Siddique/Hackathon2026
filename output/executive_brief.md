# CVE-to-My-Stack — Executive Brief

## Summary
- **Assets mapped:** 12
- **Assets unmapped:** 0
- **Prioritised CVEs shown:** 50
- **KEV (actively exploited) in list:** 30

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

1. **CVE-2025-59287** — Windows Server 2022 21H2 (CVSS 9.8, EPSS 0.7270, KEV yes)
   - CVE-2025-59287 affects Windows Server 2022 21H2. EPSS 0.7270 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
2. **CVE-2025-33053** — Windows Server 2022 21H2 (CVSS 8.8, EPSS 0.5028, KEV yes)
   - CVE-2025-33053 affects Windows Server 2022 21H2. EPSS 0.5028 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
3. **CVE-2025-2783** — Google Chrome Latest (CVSS 8.3, EPSS 0.4686, KEV yes)
   - CVE-2025-2783 affects Google Chrome Latest. EPSS 0.4686 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
4. **CVE-2025-33073** — Windows Server 2022 21H2 (CVSS 8.8, EPSS 0.3716, KEV yes)
   - CVE-2025-33073 affects Windows Server 2022 21H2. EPSS 0.3716 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
5. **CVE-2025-26633** — Windows Server 2022 21H2 (CVSS 7.0, EPSS 0.4398, KEV yes)
   - CVE-2025-26633 affects Windows Server 2022 21H2. EPSS 0.4398 indicates high exploitation probability. Actively exploited in the wild (CISA KEV).
6. **CVE-2025-30397** — Windows Server 2022 21H2 (CVSS 7.5, EPSS 0.2074, KEV yes)
   - CVE-2025-30397 affects Windows Server 2022 21H2. EPSS 0.2074 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
7. **CVE-2025-10585** — Google Chrome Latest (CVSS 9.8, EPSS 0.0154, KEV yes)
   - CVE-2025-10585 affects Google Chrome Latest. EPSS 0.0154 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
8. **CVE-2025-21418** — Windows Server 2022 21H2 (CVSS 7.8, EPSS 0.1327, KEV yes)
   - CVE-2025-21418 affects Windows Server 2022 21H2. EPSS 0.1327 indicates moderate exploitation probability. Actively exploited in the wild (CISA KEV).
9. **CVE-2025-5419** — Google Chrome Latest (CVSS 8.8, EPSS 0.0383, KEV yes)
   - CVE-2025-5419 affects Google Chrome Latest. EPSS 0.0383 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).
10. **CVE-2025-13223** — Google Chrome Latest (CVSS 8.8, EPSS 0.0280, KEV yes)
   - CVE-2025-13223 affects Google Chrome Latest. EPSS 0.0280 indicates low exploitation probability. Actively exploited in the wild (CISA KEV).

## Limitations
- Wrong product mapping → CVE may be missing silently.
- EPSS is predictive, not proof of safety.
- Not in KEV ≠ unexploited.
- Version ranges are not matched in this MVP.
