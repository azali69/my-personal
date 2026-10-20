import java.io.*;
public class H {
  static String readAll(InputStream in) throws IOException { try (InputStream i=in){ ByteArrayOutputStream bo=new ByteArrayOutputStream(); byte[] b=new byte[16384]; int n; while((n=i.read(b))>0) bo.write(b,0,n); return new String(bo.toByteArray(), java.nio.charset.StandardCharsets.UTF_8);} }
  public static void main(String[] a) throws Exception {
    String text=a[0]; String out;
    java.net.CookieManager cm = new java.net.CookieManager();
    String ua = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36";
    java.net.URL pu = new java.net.URL("https://halal.muis.gov.sg/halal/establishments");
    java.net.HttpURLConnection c = (java.net.HttpURLConnection) pu.openConnection();
    c.setRequestProperty("User-Agent", ua); c.setConnectTimeout(15000); c.setReadTimeout(20000);
    String page = readAll(c.getInputStream());
    java.util.List<String> sc = c.getHeaderFields().get("Set-Cookie"); if (sc != null) for (String h : sc) for (java.net.HttpCookie hc : java.net.HttpCookie.parse(h)) cm.getCookieStore().add(pu.toURI(), hc);
    java.util.regex.Matcher m = java.util.regex.Pattern.compile("name=\"__RequestVerificationToken\" type=\"hidden\" value=\"([^\"]+)\"").matcher(page);
    if (!m.find()) throw new Exception("token");
    StringBuilder ck = new StringBuilder(); for (java.net.HttpCookie hc : cm.getCookieStore().getCookies()) { if (ck.length() > 0) ck.append("; "); ck.append(hc.getName()).append('=').append(hc.getValue()); }
    java.net.HttpURLConnection p = (java.net.HttpURLConnection) new java.net.URL("https://halal.muis.gov.sg/api/halal/establishments").openConnection();
    p.setRequestMethod("POST"); p.setDoOutput(true);
    p.setRequestProperty("User-Agent", ua); p.setRequestProperty("Content-Type", "application/json"); p.setRequestProperty("Accept", "application/json");
    p.setRequestProperty("X-CSRF-TOKEN", m.group(1)); p.setRequestProperty("Referer", pu.toString()); p.setRequestProperty("Cookie", ck.toString());
    try (OutputStream os = p.getOutputStream()) { os.write(("{\"text\":\""+text+"\"}").getBytes("UTF-8")); }
    System.out.println("code "+p.getResponseCode()+" cookies="+ck.length());
    out = readAll(p.getInputStream()); System.out.println(out.substring(0,Math.min(400,out.length())));
  }
}
