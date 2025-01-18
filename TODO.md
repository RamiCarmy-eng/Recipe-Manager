# Recipe-Master Debug Plan

## Current Status (As of Last Session)
- Basic functionality working
- All changes saved in Git
- Working on `debug-features` branch
- Main code preserved in other branches

## Issues to Fix
1. **Recipe View Issues**
   - Problem: Shows only headers without content
   - Files: 
     - `main.py` (view_recipe function)
     - `templates/recipe.html`
   - Status: Partially working

2. **Recipe List Issues**
   - Problem: Missing images in recipe list
   - Files:
     - `templates/recipes.html`
     - `main.py` (recipes route)
   - Status: List shows but without images

3. **Add Recipe Error**
   - Problem: CategoryHelper error when clicking Add Recipe
   - Error: 'CategoryHelper' object has no attribute 'get_available_ingredients'
   - Files:
     - `main.py`
     - CategoryHelper class
   - Status: Not working

4. **Navigation Issues**
   - Problem: Missing tabs (Manage Recipes, Manage Users, Shopping List)
   - Files:
     - `templates/base.html`
   - Status: Basic navigation working, needs completion

## Starting Steps
1. Verify branch:
   ```bash
   git status  # Should show on debug-features branch
   ```

2. Start with recipe view fix:
   - Check view_recipe function in main.py
   - Verify template variables
   - Test recipe detail display

## Git Commands to Remember
- Check branch: `git status`
- Save changes: `git add .` then `git commit -m "message"`
- Switch to main if needed: `git checkout main`
- Return to debug: `git checkout debug-features`

## Notes
- Don't merge to main until all fixes are tested
- Keep track of any new issues found
- Test each fix before moving to next issue 