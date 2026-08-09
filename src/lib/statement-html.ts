import DOMPurify from "isomorphic-dompurify";

/**
 * Problem statements are scraped HTML from Codeforces, rendered with
 * `dangerouslySetInnerHTML`, so they are sanitized before they reach the DOM.
 * The allowlist is deliberately wide enough for statement markup — including
 * the MathJax spans the scraper keeps and the KaTeX we substitute for them —
 * and drops only scripts, event handlers and other active content.
 */
export function sanitizeStatementHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    // MathML + SVG are part of KaTeX's output.
    USE_PROFILES: { html: true, mathMl: true, svg: true },
    ADD_ATTR: ["aria-hidden", "style"],
    FORBID_TAGS: ["style"],
  });
}
