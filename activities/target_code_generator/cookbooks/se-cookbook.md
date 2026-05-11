- Always use Angular Reactive Forms for creating forms
- The functionality from source client must be migrated. It is crucial to have complete functional equivalence between source client and the one written by you.
- Never use inline styles in HTML. All styles must be written into SCSS files.
- Do not use external classes, services or functions if you don't find them anywhere declared in the files in the file system.
- No implicit typing is allowed. TypeScript strict mode is turned on, so make sure to handle possible null values.
- For HTTP requests, instead of using the HttpClient directly, use the post() method in the api/post.service.ts class.
- Always use <row> instead of <form-row>
- Methods should always provide a functionality and not be empty or only include a console.log/print function
- Form fiels should be set as "required/not reqiured" according to the swing files, the default should be "not required"
- Make sure to use the correct import path for the imported API services, which is 2 levels above. For example for the PocService, like this: `../../api/post.service`

# Logic
After a response is received from the service, make sure to display the data using response.data, so it looks something like this:
```
this.pocForm.patchValue({ textArea: (response as any).data });
```

# Styling

Use the ng-bootstrap Library for styling. It is already available in the package.json.

Make sure to use the Bootstrap grid layout with multiple columns!

Use the following colors:
- #b30920 for primary button color
- rgba(2, 14, 37, .08) for secondary button
- rgb(249, 251, 252) for the background

On the very top of the page there should be a horizontal banner with styling: #e70000 linear-gradient(90deg,#e70000 0,#b30920) on which in white letters our title is displayed (the name of the application).

Make it look pretty, with enough spacing and padding and such. Make use of the ng-bootstrap library.