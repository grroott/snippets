curl -k -X POST "https://yourtenant.sharepoint.com/sites/yoursite/_api/contextinfo" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json;odata=verbose" \
  -H "Content-Type: application/json;odata=verbose"


curl -k -X POST \
  "https://yourtenant.sharepoint.com/sites/yoursite/_api/web/GetFolderByServerRelativeUrl('/sites/yoursite/Shared Documents/Folder/Subfolder')/Files/add(url='filename.txt',overwrite=true)" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-RequestDigest: 0x...REAL_DIGEST..." \
  -H "Accept: application/json;odata=verbose" \
  --data-binary "@C:/path/to/filename.txt"
