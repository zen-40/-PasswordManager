# -PasswordManager
Django application layout.


My django application consists of 3 main elements.

1.)Home site

2.)Login panel, user registration, and logout.

3.)Management panel (Visible only for logged in users limited by '@login_required')


In the login panel:

a.)home page where is all password objects with functions such as:

>page name, username, page link, button that opens the link in a new tab, button showing and hiding the password (for greater security).

b.)Website for managing objects:

>the ability to add a comfortable object at the top of the page.

>below are the objects available on the page with what options:

*delete object

*edit object

*share the object (without using a database, a link valid only 5 min, everything is done via a specially encrypted link)
