# MEasyMate Launch Readiness

Production domain: `https://measymate.com`

## Launch model
- Development branch: `dev-v2`
- Production branch: `main`
- Hosting target: GitHub Pages
- Custom domain file: `CNAME` -> `measymate.com`
- Static Pages compatibility: `.nojekyll`

## QA gates before production
- Internal HTML links/assets resolve locally.
- Canonical URLs use `https://measymate.com/`.
- `robots.txt` points to the production sitemap.
- `sitemap.xml` uses the production domain.
- No old `measy.com` domain remains in HTML.
- No internal Phase 1 template copy remains.
- No generic `Download / Buy / Contact` CTA remains on unavailable products.
- Mobile Homepage, Products, Product Detail, and representative Internal Pages have been reviewed.

## Production sequence
1. Final QA on `dev-v2`.
2. Fast-forward `main` to the verified `dev-v2` commit.
3. Configure GitHub Pages to deploy from `main` / root.
4. Set custom domain to `measymate.com`.
5. Configure DNS at the domain provider.
6. Verify HTTPS and both apex/www behavior.
7. Run post-launch smoke test.
