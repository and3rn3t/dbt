# GitHub Directory

This directory contains GitHub-specific configuration files, including instructions for AI coding assistants.

## Files in this Directory

### `copilot-instructions.md`

**Purpose**: Provides comprehensive context to GitHub Copilot about this project

**Contains**:

- Project overview and tech stack
- Coding standards and conventions
- Common patterns and examples
- Best practices for Python, SQL, and notebooks
- Security guidelines
- Performance tips
- Troubleshooting guides

**How it's used**: GitHub Copilot automatically reads this file to understand your project context and provide better suggestions.

### `AI_WORKSPACE_CONTEXT.md`

**Purpose**: Additional context document for AI assistants with practical examples

**Contains**:

- Current project state
- Sample data descriptions
- Common task patterns with full code examples
- Data flow diagrams
- Naming conventions
- Error handling patterns
- Visualization preferences
- Example prompts that work well

**How it's used**: Reference document for when you need AI help with specific tasks. Copy relevant sections into your prompts.

## How to Use These Files

### 1. Let Copilot Read Automatically

GitHub Copilot automatically reads `copilot-instructions.md` when making suggestions. No action needed!

### 2. Reference in Chat

When asking questions in GitHub Copilot Chat or other AI assistants:

```
"Following the patterns in .github/copilot-instructions.md, 
create a dbt staging model for customer data"
```

### 3. Copy Examples

Use the examples in `AI_WORKSPACE_CONTEXT.md` as starting points:

- Copy the pattern that matches your task
- Adapt it to your specific needs
- AI assistants will maintain the coding style

### 4. Update as Needed

As your project evolves, update these files:

- Add new patterns you've established
- Document new conventions
- Include lessons learned
- Add common error solutions

## Benefits

✅ **More Accurate Suggestions**: Copilot understands your project structure and conventions

✅ **Consistent Code Style**: All AI-generated code follows your standards

✅ **Better Context**: AI knows about your data, models, and workflow

✅ **Faster Development**: Spend less time explaining, more time building

✅ **Team Alignment**: New team members and AI follow the same patterns

## Tips for Best Results

1. **Be Specific**: Reference specific patterns when asking for help

   ```
   "Create a data loading function following the pattern in copilot-instructions.md"
   ```

2. **Provide Context**: Mention relevant files or data

   ```
   "Analyze the sample_sales_data.csv file using our standard EDA pattern"
   ```

3. **Use Examples**: Reference examples from the context files

   ```
   "Like the mart_sales_summary example, create a mart for customer metrics"
   ```

4. **Iterate**: Start with generated code, then refine

   ```
   "Good, now add error handling following our error handling patterns"
   ```

## Maintaining These Files

### When to Update

- ✅ New coding patterns emerge
- ✅ Tech stack changes
- ✅ New data sources added
- ✅ Common issues discovered
- ✅ Best practices evolve

### What to Include

- ✅ Patterns you use repeatedly
- ✅ Project-specific conventions
- ✅ Common pitfalls and solutions
- ✅ Important context about data/models
- ✅ Security and privacy requirements

### What NOT to Include

- ❌ Sensitive information (credentials, keys)
- ❌ Personal identifiable information
- ❌ Internal business logic
- ❌ Temporary or experimental code
- ❌ Overly specific implementation details

## Example Workflows

### Creating a New Analysis Notebook

1. **Prompt Copilot**:

   ```
   "Create a new Jupyter notebook for analyzing customer churn 
   using the notebook structure pattern from copilot-instructions.md"
   ```

2. **Copilot generates**: Notebook with proper structure, imports, and patterns

3. **You customize**: Add your specific analysis logic

### Adding a New dbt Model

1. **Prompt Copilot**:

   ```
   "Create a dbt staging model for orders data following 
   the stg_source_entity pattern with data validation"
   ```

2. **Copilot generates**: SQL file with CTEs, proper naming, and structure

3. **You review**: Check logic and add business rules

### Writing a Data Fetching Script

1. **Prompt Copilot**:

   ```
   "Create a script to fetch data from an API and save to raw/ 
   following the fetch pattern with error handling"
   ```

2. **Copilot generates**: Script with retry logic, error handling, and proper paths

3. **You configure**: Add API endpoint and authentication

## Integration with Other Tools

### VS Code Settings

The `.vscode/settings.json` file is configured to work with:

- GitHub Copilot
- Python language server
- Jupyter notebooks
- Data Wrangler

### Pre-commit Hooks

The `.pre-commit-config.yaml` ensures code follows standards before committing

### Code Formatters

Black, isort, and flake8 ensure all code (AI-generated or not) follows conventions

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [Best Practices for Copilot](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
- [VS Code Copilot Guide](https://code.visualstudio.com/docs/copilot/overview)

## Questions?

- **Project structure**: See `CONFIGURATION.md`
- **Data science setup**: See `DATA_SCIENCE_GUIDE.md`
- **Quick reference**: See `CONFIG_QUICKREF.md`
- **dbt patterns**: See `templates/README.md`

---

**Remember**: These files are your project's knowledge base for AI assistants. Keep them updated, and they'll keep helping you code faster and better! 🚀
