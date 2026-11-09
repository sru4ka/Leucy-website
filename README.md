# Leucy website

Marketing site and legal pages for **Leucy: GLP-1 Tracker**. Plain static HTML and CSS with self-hosted fonts. No cookies, no analytics, no third-party requests, no build step needed to host it.

## Pages

| URL | Page |
| --- | --- |
| `/` | Home: hero, how it works, features, medications, privacy, pricing, FAQ |
| `/privacy/` | Privacy Policy |
| `/terms/` | Terms of Use, including Apple's required App Store terms |
| `/health-data/` | Consumer Health Data Notice (Washington, Nevada, Connecticut) |
| `/medical-disclaimer/` | Medical Disclaimer |
| `/subscriptions/` | Plans, trial, auto-renewal, cancelling, refunds |
| `/delete-data/` | How to delete device data, the account and its backup (use this as the data deletion URL in store listings) |
| `/support/` | Contact and FAQ |
| `/legal/` | Index of every policy |

## Editing

Page content lives in `src/*.html`. The shared head, header and footer live in `tools/build.py`, along with the site settings at the top of that file: domain, support email, App Store link and effective date.

After editing, rebuild:

```bash
python3 tools/build.py
```

Commit both `src/` and the generated pages. Setting `APP_STORE_URL` in `tools/build.py` switches every "Coming soon" button to "Download on the App Store".

Preview locally:

```bash
python3 -m http.server 8000
```

## Deploying

Any static host works. With GitHub Pages: Settings, Pages, deploy from the branch that holds these files, folder `/ (root)`. To use a custom domain, add it in the Pages settings, which creates a `CNAME` file, and point your DNS at GitHub.

Netlify, Vercel and Cloudflare Pages also work with no build command and the repo root as the output folder.

The app's `lib/config.ts` already links to `https://leucyapp.com/privacy/`, `/terms/` and `/health-data/`.

## Before launch

- [x] `SITE_URL` is `https://leucyapp.com`, and the `CNAME` file tells GitHub Pages to serve that domain.
- [ ] HTTPS: in the repo's Settings, Pages, wait until the certificate for leucyapp.com is issued, then tick "Enforce HTTPS". Until then https://leucyapp.com shows a certificate warning, and the app's Privacy and Terms links open with that warning.
- [ ] The contact email is a personal Gmail for now. Switch `SUPPORT_EMAIL` and `PRIVACY_EMAIL` to a domain address such as support@leucyapp.com when it exists.
- [ ] Add your legal business name and mailing address to the Privacy Policy and Terms if you have a company. Some laws, including GDPR, expect them.
- [ ] Confirm Delaware as the governing law in the Terms, or change it to your state.
- [ ] Confirm the retention periods in the Privacy Policy (24 months for analytics, support email and inactive accounts) match how you configure PostHog and Supabase.
- [x] The Supabase project is in a US region (us-east-1), as the policies say backups are stored in the United States.
- [x] Account deletion: the app has Delete account (Profile, Account and backup), which removes the account and its backup on the server. `/delete-data/` describes it.
- [ ] Paste the App Store link into `APP_STORE_URL` once the app is approved.
- [ ] Have a lawyer review the policies. They were written to match how the app works, but they are not legal advice.

App screenshots in `assets/img/app/` are real screens from the Leucy app, captured with sample data. Food and lifestyle photos come from the app's own assets.

Fonts: Fraunces and Inter, both under the SIL Open Font License (see `assets/fonts/`).
