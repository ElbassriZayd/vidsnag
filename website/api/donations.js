// Serverless: counts incoming USDT (BEP20) donations to the address this month.
// Moralis key stays server-side (env var) so it's never exposed in the frontend.
// Edge-cached 5 min to stay well within the free Moralis quota.
const ADDR = "0xd62212b2CE5f5AEf16A5b79B5e00Fa02AA68fB33";
const USDT = "0x55d398326f99059fF775485246999027B3197955"; // USDT BEP20

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate=900");
  const KEY = process.env.MORALIS_KEY;
  if (!KEY) return res.status(200).json({ count: 0, total: 0 });
  try {
    const now = new Date();
    const fromDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1)).toISOString();
    const url = `https://deep-index.moralis.io/api/v2.2/${ADDR}/erc20/transfers`
      + `?chain=bsc&token_addresses%5B0%5D=${USDT}`
      + `&from_date=${encodeURIComponent(fromDate)}&order=DESC&limit=100`;
    const r = await fetch(url, { headers: { "X-API-Key": KEY, accept: "application/json" } });
    if (!r.ok) throw new Error("moralis " + r.status);
    const j = await r.json();
    const incoming = (j.result || []).filter(
      t => (t.to_address || "").toLowerCase() === ADDR.toLowerCase());
    const total = incoming.reduce(
      (s, t) => s + Number(t.value_decimal != null ? t.value_decimal : Number(t.value) / 1e18) || s, 0);
    res.status(200).json({ count: incoming.length, total });
  } catch (e) {
    res.status(200).json({ count: 0, total: 0 });
  }
}
