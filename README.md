# cyber security mooc project

[Course page](https://cybersecuritybase.mooc.fi/module-3.1)

[Testing instructions](https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/installation.md)

[Course essay with security flaw description](https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/course_essay.md)

This is a course project to demostrate different software security flaws and how to fix them. The assignment was to choose five flaws from [OWASP Top Ten list](https://owasp.org/www-project-top-ten/#), explain how each flaw in present in the code and write fix for it.

I am using an old course project as a template. This app is for creating an overnight oats recipe bank. User can create an account, add a new recipe, comment a recipe, add it to favorites and search recipes by name or ingredient. Especially the adding recipe function is quite rigid and not really usefull, but as the original course was about creating a webapp with database it filled its purpose.


### Known issues in the application:

- As a recipe bank, there is one big problem of fundamental quality here: the user cannot enter his own recipe in its entirety, but has to choose the ingredients from a (quite limited) list. However, I stuck to this because the purpose of the course was specifically to practice the database application, and by limiting free text inputs it was easier to manage. The recipe instructions are also generic and do not give room for the user's own ideas, e.g. "flame the oatmeal before adding it to the bowl".- 
- If the main user has not published any recipe of the week, the button 'Recipe of the week' on the main page does not give an error message but shows the empty body of the recipe
- When adding a new recipe, the application checks whether there is already a recipe with the same name in the database. The function has been clumsily implemented so that the script of the html page does not recognize the error, but it only appears as a separate error notification page just before it is exported. In addition, the application fetches all the recipes in the database every time the user starts to create a new recipe, which is a resource-wasting option, but I ended up with it when I couldn't come up with anything better.
- The application does not have a floating main menu that would appear on every page, but is added separately to each html template with minor variations.
