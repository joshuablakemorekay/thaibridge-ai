// Forwards the oldest address, thaibridge-ai.smoald.com, to the app's
// current home. It lives here, on Cloudflare, because Render's free plan
// only allows two custom addresses and those go to the newer ones.
//
// Page visits get a permanent 301, so Google moves its listing across.
// Anything else (a form post) gets a 308, which keeps the method and body.
const NEW_ORIGIN = 'https://jaiway.smoald.com';

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const status = ['GET', 'HEAD'].includes(request.method) ? 301 : 308;
    return Response.redirect(NEW_ORIGIN + url.pathname + url.search, status);
  },
};
