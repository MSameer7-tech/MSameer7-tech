# MSameer7-tech Animated GitHub Profile

This folder is a customized version of the `navi3582/animated-github-profile` approach.

## 1. Create the profile repository

Create a **public** GitHub repository named exactly:

`MSameer7-tech`

GitHub displays its root `README.md` on your profile when the repository name matches your username and the repository is public.

## 2. Install local dependencies

From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
pip install -r scripts/requirements-portrait.txt
```

## 3. Add your photo

Copy a clear, well-lit head-and-shoulders photo into this folder, for example:

```text
sameer.jpg
```

Then run:

```bash
python scripts/prep_photo.py sameer.jpg
python scripts/make_ascii_svg.py
```

This creates:

```text
source-prepped.png
ascii-portrait.svg
```

## 4. Generate your info card

The information is already customized in:

```text
scripts/make_info_card.py
```

Run:

```bash
python scripts/make_info_card.py
```

This creates:

```text
info-card.svg
```

## 5. Generate the contribution graph

Run:

```bash
GITHUB_USERNAME=MSameer7-tech python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

This creates:

```text
data/contributions.json
contrib-heatmap.svg
```

## 6. Push to GitHub

The repository should contain:

```text
MSameer7-tech/
├── .github/
│   └── workflows/
│       └── update-profile-art.yml
├── data/
│   └── contributions.json
├── scripts/
│   ├── fetch_contributions.py
│   ├── make_ascii_svg.py
│   ├── make_info_card.py
│   ├── prep_photo.py
│   ├── render_heatmap_svg.py
│   ├── requirements.txt
│   └── requirements-portrait.txt
├── README.md
├── ascii-portrait.svg
├── contrib-heatmap.svg
├── info-card.svg
└── source-prepped.png
```

You can omit `source-prepped.png` if you do not want to store the intermediate photo asset in GitHub.

Then:

```bash
git add .
git commit -m "Create animated profile"
git push origin main
```

## 7. Enable Actions write permissions

On GitHub:

`Settings → Actions → General → Workflow permissions`

Select:

`Read and write permissions`

Save the setting.

Then go to:

`Actions → Update profile art → Run workflow`

The workflow will regenerate the contribution graph.

After that, the scheduled job runs daily.

## 8. Updating your portrait

Whenever you want to change the portrait:

```bash
python scripts/prep_photo.py new-photo.jpg
python scripts/make_ascii_svg.py
git add source-prepped.png ascii-portrait.svg
git commit -m "Update profile portrait"
git push
```

## 9. Updating your information

Edit:

```text
scripts/make_info_card.py
```

Change the `ROWS` list, then:

```bash
python scripts/make_info_card.py
git add info-card.svg scripts/make_info_card.py
git commit -m "Update profile information"
git push
```
