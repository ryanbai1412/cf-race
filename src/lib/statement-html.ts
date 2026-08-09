import DOMPurify from "dompurify";

/**
 * Problem statements are scraped HTML from Codeforces, rendered with
 * `dangerouslySetInnerHTML`, so they are sanitized before they reach the DOM.
 * The allowlist is deliberately wide enough for statement markup — including
 * the MathJax spans the scraper keeps and the KaTeX we substitute for them —
 * and drops only scripts, event handlers and other active content.
 *
 * Browser-only: DOMPurify needs a real DOM, so on the server this yields the
 * empty string and `StatementPane` renders the statement after mount rather
 * than shipping unsanitized markup in the SSR payload.
 */
export function sanitizeStatementHtml(html: string): string {
  if (!DOMPurify.isSupported) return "";
  return DOMPurify.sanitize(html, {
    // MathML + SVG are part of KaTeX's output.
    USE_PROFILES: { html: true, mathMl: true, svg: true },
    ADD_ATTR: ["aria-hidden", "style"],
    FORBID_TAGS: ["style"],
  });
}
