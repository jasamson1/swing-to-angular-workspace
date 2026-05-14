## Code Guidelines

# Form Handling
- Use Angular Reactive Forms exclusively.
- Form fields must be marked as required or not required based on the Swing files. Default is not required.
- Use <row> instead of <form-row> for layout.
- Ensure functional equivalence with the source client — all features must be migrated and work identically.
- If Radio Buttons are used, one option should always be selected as default.
  
# Code Quality
- No inline styles in HTML — all styles must go into .scss files.
- No implicit typing — TypeScript strict mode is enabled. Handle all null or undefined values explicitly.
- Do not use external classes/services/functions unless they are declared in the file system.
- Remove unused or incorrect imports.
- Methods must be functional — no empty methods or ones with only console.log.
  
# HTTP Requests
- Use the post() method from api/post.service.ts instead of HttpClient directly. It should look like this: ```this.postService.post(this.pocForm.value)```
Import API services using the correct relative path: `../../api/post.service`


# Response Handling
- After a response is received from the service, make sure to display the data using response.data. It should look like this: ```this.pocForm.patchValue({ textArea: (response as any).data });```


## Styling Guidelines

# Layout
- Use Bootstrap grid layout with multiple columns.
- Use ng-bootstrap components for UI elements (already included in package.json).
- Spacing: Adequate padding and margin for a clean look
- Make use of the ng-bootstrap library.
  
# Colors
- Primary button: #b30920
- Secondary button: rgba(2, 14, 37, .08)
- Background: rgb(249, 251, 252)
  
# Top Banner
- There should be a horizontal banner at the top of the page with:
  - Background: #e70000 linear-gradient(90deg, #e70000 0%, #b30920)
  - Text: White, displaying the application title
  