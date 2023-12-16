1. app.py

@app.route('/login', methods=["GET", "POST"])
def login()

added `session['username']=user.username` in
if user:
do_login(user)
flash(f"Hello, {user.username}!", "success")
session['username']=user.username
return redirect("/")

2. base.html

added `{% if not session['username'] %}` instead of `{% if not g.user %}` in
{% endif %} {% if not session['username'] %}

<li><a href="/signup">Sign up</a></li>
<li><a href="/login">Log in</a></li>

3. detail.html

replaced this `<div id="warbler-hero" class="full-width"></div>` for this

<img
  src="{{ user.header_image_url }}"
  alt="Image for {{ user.username }}"
  id="warbler-hero"
  class="full-width"
/>

4. added 'overlaps' here because these relationships link with the same column in User:
   followers = db.relationship(
   "User",
   secondary="follows",
   primaryjoin=(Follows.user_being_followed_id == id),
   secondaryjoin=(Follows.user_following_id == id),
   overlaps="following"
   )

   following = db.relationship(
   "User",
   secondary="follows",
   primaryjoin=(Follows.user_following_id == id),
   secondaryjoin=(Follows.user_being_followed_id == id),
   overlaps='followers'
   )

5. home.html

in <button
            class="
                btn 
                btn-sm 
                {{'btn-primary' if msg.id in likes else 'btn-secondary'}}"
          >
edited `{{'btn-primary' if msg.id in likes else 'btn-secondary'}}` for `{{'btn-primary' if msg in user.likes else 'btn-secondary'}}"`
