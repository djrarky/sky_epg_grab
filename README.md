# Sky EPG Grabber

This Docker container fetches Sky TV EPG data for a specified UK region and serves it as an XMLTV file via HTTP.

## Features

- Fetches up to 7 days of EPG data
- Includes Program titles, descriptions and images
- Auto-refreshes on a defined schedule
- Serves `sky.xml` over HTTP (`http://localhost:8855/sky.xml`)
- Configurable region, EPG length, and refresh rate

## Docker Run

```bash
docker run -d \
  --name sky_epg_grab \
  -p 8855:8855 \
  -e REGION=7 \
  -e EPG_DAYS=7 \
  -e REFRESH_HOURS=48 \
  --restart unless-stopped \
  ghcr.io/djrarky/m3u-epg-sync:latest
```
## Docker Compose
```yaml
services:
  sky_epg_grab:
    image: ghcr.io/djrarky/m3u-epg-sync:latest
    container_name: sky_epg_grab
    ports:
      - "8855:8855"
    environment:
      REGION: 7          # 1 for London (default), 2 for Essex, 3 for Central Midlands...
      EPG_DAYS: 7        # Number of days of guide data to grab (1–7 days) - 7 days is default
      REFRESH_HOURS: 48   # How often to refresh the EPG - 6 hours is the default.
    restart: unless-stopped
```
## Environment Variables
|    Variable   | Default | Description |
|:-------------:|:-------:|:------------|
| REGION        | 1       | Sky TV region ID. Visit [sky.com/tv-guide](https://www.sky.com/tv-guide), choose your region, and check the URL for `4101-x` — `x` is your region number. Example: `1` = London HD, `2` = Essex HD |
| EPG_DAYS      | 7       | Number of days of EPG to fetch (1–7) |
| REFRESH_HOURS | 6       | How often to update the XML (in hours) |

## Credit
Based on [Plebster/sky_epg_grab](https://github.com/Plebster/sky_epg_grab) & [GitHub: jtee3d/sky_epg_grab](https://github.com/jtee3d/sky_epg_grab)
