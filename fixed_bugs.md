app.py

@app.route('/login', methods=["GET", "POST"])
def login()

added `session['username']=user.username` in
if user:
do_login(user)
flash(f"Hello, {user.username}!", "success")
session['username']=user.username
return redirect("/")

base.html

added `{% if not session['username'] %}` instead of `{% if not g.user %}` in
{% endif %} {% if not session['username'] %}

<li><a href="/signup">Sign up</a></li>
<li><a href="/login">Log in</a></li>

detail.html

replaced this `<div id="warbler-hero" class="full-width"></div>` for this

<img
  src="{{ user.header_image_url }}"
  alt="Image for {{ user.username }}"
  id="warbler-hero"
  class="full-width"
/>
