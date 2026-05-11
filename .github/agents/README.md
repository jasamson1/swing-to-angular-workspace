# Swing to Angular Migration Agents

This directory contains AI agents that orchestrate and execute the complete migration of Java Swing MVP applications to Angular 16+.

## Agent Architecture

The migration system uses a **hierarchical agent architecture** with one orchestrator agent coordinating three specialized sub-agents:

```
┌─────────────────────────────────────────────────────┐
│   Swing to Angular Migration Orchestrator          │
│   (swing-to-angular-orchestrator.agent.md)         │
│                                                     │
│   - Plans complete migration workflow              │
│   - Discovers Java Swing components                │
│   - Coordinates sub-agents                         │
│   - Monitors progress and quality                  │
│   - Generates migration reports                    │
└──────────────┬──────────────────────────────────────┘
               │
               │ Delegates tasks to:
               │
       ┌───────┴───────┬─────────────┬──────────────┐
       │               │             │              │
       ▼               ▼             ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Software   │ │  Software   │ │   DevOps    │
│  Engineer   │ │  Reviewer   │ │  Engineer   │
│   Agent     │ │   Agent     │ │   Agent     │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Agent Descriptions

### 1. Swing to Angular Migration Orchestrator
**File**: `swing-to-angular-orchestrator.agent.md`  
**Type**: Top-level orchestration agent (`infer: false`)  
**Tools**: `agent`, `read`, `search`, `edit`, `execute`

**Purpose**: Manages the complete end-to-end migration process from environment setup through final build verification.

**Responsibilities**:
- Environment preparation and validation
- Java Swing component discovery (scanning for MVP triplets)
- Angular project initialization coordination
- Migration workflow orchestration
- Quality assurance through iterative review cycles
- Final build verification
- Migration report generation

**When to use**: This is the entry point for all Swing to Angular migrations. Users interact with this agent to start the migration process.

---

### 2. Swing to Angular Software Engineer
**File**: `swing-to-angular-engineer.agent.md`  
**Type**: Inferred sub-agent (`infer: true`)  
**Tools**: `read`, `search`, `edit`

**Purpose**: Translates Java Swing MVP source code into Angular components with functional equivalence.

**Responsibilities**:
- Generate HTML templates from Swing Views
- Generate TypeScript components from Swing Presenters/Models
- Generate SCSS styling from Swing appearance
- Apply fixes based on Software Reviewer feedback
- Ensure adherence to Angular best practices

**Key Standards**:
- Angular Reactive Forms for all forms
- No inline styles (all styling in SCSS)
- Bootstrap 5 + ng-bootstrap components
- TypeScript strict type safety
- Specific color scheme (#b30920, rgba(2,14,37,.08), rgb(249,251,252))
- API integration via `../../api/post.service`

**When used**: Orchestrator delegates to this agent whenever Angular code needs to be generated or modified.

---

### 3. Swing to Angular Software Reviewer
**File**: `swing-to-angular-reviewer.agent.md`  
**Type**: Inferred sub-agent (`infer: true`)  
**Tools**: `read`, `search`

**Purpose**: Validates generated Angular code for functional equivalence, quality, and adherence to standards.

**Responsibilities**:
- Review HTML templates, TypeScript components, and SCSS files
- Verify functional equivalence with Swing source
- Check adherence to coding standards and best practices
- Identify errors, missing functionality, and deviations
- Provide specific, actionable feedback
- Document findings in detailed changelogs

**Review Criteria**:
- Functional equivalence with Swing
- Angular Reactive Forms implementation
- Type safety (no implicit `any`)
- Styling standards (no inline styles, correct colors)
- Import paths and dependencies
- Form validation correctness
- HTTP/API integration patterns
- Method completeness (no empty methods)

**When used**: Orchestrator delegates to this agent after each component generation to ensure quality before proceeding.

**Important**: This agent NEVER modifies code—it only identifies issues and proposes fixes.

---

### 4. Swing to Angular DevOps Engineer
**File**: `swing-to-angular-devops.agent.md`  
**Type**: Inferred sub-agent (`infer: true`)  
**Tools**: `read`, `search`, `edit`, `execute`

**Purpose**: Manages Angular project infrastructure, builds, and deployment automation.

**Responsibilities**:
- Create and configure Angular projects (ng new)
- Generate component skeletons (ng generate)
- Install npm dependencies (Bootstrap, ng-bootstrap)
- Generate OpenAPI client services
- Configure build settings (angular.json)
- Run production builds (ng build)
- Troubleshoot infrastructure issues
- Report compilation errors with context

**Key Operations**:
- Angular CLI project creation
- npm dependency management
- OpenAPI code generation
- Build verification and error reporting
- Development server management

**When used**: Orchestrator delegates to this agent for project setup, component scaffolding, dependency installation, and build verification.

**Important**: This agent handles infrastructure but NEVER fixes application code—it reports code errors to the orchestrator for delegation to the Software Engineer.

---

## Migration Workflow

The typical migration follows this workflow:

```
1. User initiates migration
   └─> Orchestrator Agent activated

2. Orchestrator validates environment and discovers components
   └─> Scans Java source for *View.java, *Model.java, *Presenter.java

3. Orchestrator → DevOps Engineer: Setup project
   └─> Create Angular project, install dependencies, configure build

4. For each discovered component:
   
   4.1. Orchestrator reads Swing source files
   
   4.2. Orchestrator → DevOps Engineer: Generate component skeleton
        └─> ng generate component
   
   4.3. Orchestrator → Software Engineer: Generate HTML template
        └─> Translate Swing View to Angular HTML
   
   4.4. Orchestrator → Software Engineer: Generate TypeScript component
        └─> Translate Swing Presenter/Model to Angular TypeScript
   
   4.5. Orchestrator → Software Engineer: Generate SCSS styling
        └─> Create styling matching Swing appearance
   
   4.6. Orchestrator → Software Reviewer: Review component
        └─> Validate quality and functional equivalence
   
   4.7. If issues found:
        4.7.1. Orchestrator → Software Engineer: Apply fixes
        4.7.2. Orchestrator → Software Reviewer: Re-review
        4.7.3. Repeat until approved
   
   4.8. Move to next component

5. Orchestrator → DevOps Engineer: Build project
   └─> ng build --configuration production

6. If build errors:
   6.1. DevOps Engineer reports errors to Orchestrator
   6.2. Orchestrator → Software Engineer: Fix errors
   6.3. Orchestrator → DevOps Engineer: Rebuild
   6.4. Repeat until build succeeds

7. Orchestrator generates migration report
   └─> Complete documentation of migration results

8. Handoff to user
   └─> Provide project location, next steps, testing guidance
```

## Environment Variables Required

The agents expect these environment variables to be configured:

| Variable | Description | Example |
|----------|-------------|---------|
| `ORIGIN_PROJECT_PATH` | Path to Java Swing source project | `C:\projects\swing-app` |
| `TARGET_PROJECT_PATH` | Path where Angular project will be created | `C:\projects\migrated` |
| `ANGULAR_APP_NAME` | Name for the Angular application | `swing-app-angular` |
| `ANGULAR_PROJECT_PATH` | Full path to Angular project | `C:\projects\migrated\swing-app-angular` |
| `ORIGIN_TECHNOLOGY` | Source technology | `Java Swing MVP` |
| `TARGET_TECHNOLOGY` | Target technology | `Angular` |
| `COMPILER_TECHNOLOGY` | Build system | `Angular CLI` |
| `OPENAPI_FILE_PATH` | Path to OpenAPI spec (optional) | `C:\specs\api.yml` |
| `DELETING_OUTPUT` | Delete existing output before migration | `true` or `false` |

## Prerequisites

Before using these agents, ensure:

1. **Node.js** LTS version is installed
2. **npm** is available
3. **Angular CLI** v16.0.0 is installed globally: `npm install -g @angular/cli@16.0.0`
4. **OpenAPI Generator CLI** is installed (if using API generation): `npm install -g @openapitools/openapi-generator-cli`
5. Java Swing source project exists and follows MVP naming conventions
6. Environment variables are configured

## Agent Capabilities

### Orchestrator Agent
- ✅ Read and search workspace files
- ✅ Edit configuration files
- ✅ Execute shell commands
- ✅ Delegate to sub-agents
- ✅ Plan and coordinate complex workflows
- ✅ Generate comprehensive reports

### Software Engineer Agent
- ✅ Read Swing source files
- ✅ Search for code patterns
- ✅ Edit/create Angular component files
- ✅ Generate HTML, TypeScript, and SCSS
- ✅ Apply fixes based on feedback

### Software Reviewer Agent
- ✅ Read source and generated files
- ✅ Search for patterns and issues
- ✅ Analyze code quality
- ✅ Provide detailed feedback
- ❌ Cannot modify files (review only)

### DevOps Engineer Agent
- ✅ Read configuration files
- ✅ Search for file system issues
- ✅ Edit configuration files
- ✅ Execute build commands
- ✅ Install dependencies
- ✅ Generate project scaffolding
- ❌ Cannot fix application code

## Code Quality Standards

All generated code must meet these standards:

### TypeScript
- Explicit type definitions (no implicit `any`)
- Proper null/undefined handling
- Angular best practices
- No empty methods
- Proper error handling

### HTML Templates
- Angular Reactive Forms
- No inline styles
- Bootstrap grid layout
- ng-bootstrap components
- Proper event bindings

### SCSS Styling
- Component-scoped styles
- Specific color scheme
- Modern, responsive design
- No inline styles in HTML

### API Integration
- Use PostService from `../../api/post.service`
- Proper response handling: `(response as any).data`
- Error handling
- Correct import paths

## Output Structure

The agents produce this directory structure:

```
TARGET_PROJECT_PATH/
└── ANGULAR_APP_NAME/
    ├── node_modules/
    ├── src/
    │   ├── app/
    │   │   ├── components/
    │   │   │   ├── component1/
    │   │   │   │   ├── component1.component.ts
    │   │   │   │   ├── component1.component.html
    │   │   │   │   └── component1.component.scss
    │   │   │   └── component2/
    │   │   │       └── ...
    │   │   ├── api/ (if OpenAPI used)
    │   │   │   ├── services/
    │   │   │   └── models/
    │   │   ├── app.module.ts
    │   │   ├── app.component.ts
    │   │   └── app-routing.module.ts
    │   ├── assets/
    │   └── styles.scss
    ├── angular.json
    ├── package.json
    ├── tsconfig.json
    └── MIGRATION_REPORT.md
```

## Success Criteria

A migration is successful when:

- ✅ All Java Swing MVP components are discovered
- ✅ Angular project is created and configured
- ✅ All dependencies are installed
- ✅ All components are generated (HTML, TS, SCSS)
- ✅ All components pass software review
- ✅ Production build completes without errors
- ✅ Functional equivalence with Swing is maintained
- ✅ Migration report is generated

## Troubleshooting

### Common Issues

1. **Component Discovery Fails**
   - Verify Swing files follow naming convention: `*View.java`, `*Model.java`, `*Presenter.java`
   - Check file permissions
   - Ensure complete MVP triplets exist

2. **Build Errors**
   - Check TypeScript version compatibility
   - Verify all imports are correct
   - Ensure API services exist if referenced
   - Review DevOps Engineer error reports

3. **Code Quality Issues**
   - Review Software Reviewer feedback carefully
   - Ensure all Swing functionality is replicated
   - Verify coding standards are followed
   - Check for empty methods or placeholders

4. **Infrastructure Issues**
   - Verify Node.js and npm versions
   - Check Angular CLI installation
   - Ensure sufficient disk space
   - Verify file system permissions

## Additional Tools Required

The agents may require these tools to be available in the workspace:

### Current Tools (Already Available)
- ✅ File reading and searching
- ✅ File editing and creation
- ✅ Command execution (PowerShell/terminal)
- ✅ Sub-agent delegation (orchestrator only)

### No Additional Custom Tools Required
The agents are designed to work with standard VS Code and GitHub Copilot capabilities. They use:
- Standard file operations
- Shell command execution
- Built-in search and grep
- Text editing capabilities

### External Dependencies (User Must Install)
- Angular CLI v16.0.0
- OpenAPI Generator CLI (optional)
- Node.js LTS
- npm

No custom tools need to be added to the `tools/` directory. The agents are self-contained and use standard capabilities.

---

## Usage

To start a migration, interact with the **Swing to Angular Migration Orchestrator** agent. It will automatically coordinate the sub-agents as needed.

**Example prompt**:
```
Please migrate my Java Swing MVP application to Angular. The Swing source is in C:\projects\swing-app and I want the Angular project created in C:\projects\migrated with the name "modern-swing-app".
```

The orchestrator will:
1. Validate environment and prerequisites
2. Discover all Swing components
3. Create Angular project structure
4. Migrate each component iteratively
5. Verify builds successfully
6. Generate comprehensive report
7. Provide next steps

---

**Last Updated**: February 11, 2026  
**Agent Version**: 1.0  
**Compatible with**: GitHub Copilot, VS Code
