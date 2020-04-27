/**
 * Common Authorization functions.
 */

class Auth {
  constructor() {
    this.token = "";
  }

  /**
   * Check token on url
   */
  static check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if ( fragment[0] === 'access_token' ) {
      // add the access token to the jwt
      this.token = fragment[1];
      // save jwts to localstore
      this.set_jwt();
    }
  }

  static set_jwt() {
    localStorage.setItem("JWTS_LOCAL_KEY", this.token);
    if (this.token) {
      console.log(this.token);
    }
  }

  static activeJWT() {
    return this.token;
  }

  static logout() {
    this.token = "";
    this.set_jwt();
  }
}
