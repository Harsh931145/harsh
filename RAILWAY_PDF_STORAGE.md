# Railway PDF Storage

Uploaded PDFs are only permanent on Railway when the backend service has a
Volume attached. Without a Volume, Railway can replace the container during a
redeploy and uploaded files may disappear.

## Setup

1. Open the backend service in Railway.
2. Add a Volume to the service.
3. Use mount path: `/data`
4. Redeploy the backend.

The app automatically detects `RAILWAY_VOLUME_MOUNT_PATH` and stores PDFs in:

```text
/data/knowledgebase
```

On first start with a fresh volume, bundled PDFs from the repository are copied
into the volume without overwriting any uploaded files.

## Check

Open the backend root URL. It should show:

```json
"persistent_storage": true
```

