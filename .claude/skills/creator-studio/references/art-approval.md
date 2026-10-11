# Art review and human style approval

Read when starting manga production, changing a style, or responding to feedback such as “too AI-looking”. This is a craft review, not an AI detector and not a promise that generated art can be made indistinguishable from human work.

## Diagnose before retrying

View the actual rejected image. Record page/panel, visible defect, story effect, intended correction and invariants. “Make it less AI” alone is not a useful repair instruction. Judge choices: eye flow, silhouette, physical weight, contact anatomy, perspective, acting, information density, ink hierarchy, color emphasis and lettering. Check the image at normal reading size as well as enlarged.

Common failure patterns and corrections:

| Observation | Correction to test |
|---|---|
| Every panel is a fully rendered scenic illustration | Give an establishing shot the geography; simplify supporting backgrounds where acting or speech matters. Keep details needed for action. |
| Fur, leaves, stone and faces all have equal texture | Choose focal edges and black/color masses; suppress subordinate marks. Added paper grain is not a substitute. |
| Same rounded face, eyes and pose in every situation | Specify each character's intent, gaze and asymmetric pose; test silhouette and expression against the scene. Redesign proportions only as an explicit candidate revision. |
| Shading makes bodies shiny or toy-like | Match the project's chosen ink and color grammar; simplify value planes if that serves it. Dense rendering is valid when intentionally selected, not a universal defect. |
| Speech readable but misplaced | Put the line at its source-linked action beat; design shape, tail, emphasis and negative space together. Protect hands, eyes and action contacts. |
| “Hand-drawn” filter over generic staging | Rebuild panel hierarchy, shots, acting and line/color decisions; change the structure, not merely the prompt adjective. |

Sparse ink, grayscale, reduced eye size and 3–5 panels are possible remedies, not defaults for all genres. Do not replace a user's chosen colorful manhua with monochrome or impose this project's character design on another story. Describe broad craft techniques rather than claiming to reproduce a living artist's exact style.

## One proof, two separate judgments

For a new or rejected art direction, generate one representative real page with dialogue and action before scaling. A polished cover alone does not test sequential storytelling. View it beside identity references. Save two separate results:

- Technical inspection: exact text, speaker tails, anatomy affecting action, scene causality, identity and injuries.
- Art direction review: visible choices, acting, density, page rhythm and fit to the user's intent. Record concrete observations, remaining defects and whether human approval is pending, accepted or rejected.

A technical pass does not approve a style. Human approval must refer to a visible candidate revision. Starting the workshop or choosing an art-direction title does not approve every future rendering. If the user rejects the art, mark it rejected for production, retain the technical history, revoke any prior current production approval and stop scaling that style.

## Iteration and locking

Repair a candidate with a specific change while protecting successful parts. If a rejected rendering is itself biasing generation, separate identity invariants from its rendering and generate a fresh candidate composition. Show the inspected result for the requested human review. When the user explicitly asks to iterate until approved, continue in review rounds; do not silently treat a retry count or elapsed time as acceptance. Stop repeating unchanged prompts when no progress is visible: change the approach and state the tradeoff. Do not keep generating while the required human review is pending.

After explicit approval, record style revision, actual anchor-image path/hash, human approval text/date, character versions, line/color/density/lettering rules and project-specific avoidances. Update the project's style recipe and reference pack using the approved image. Keep the reusable skill focused on the review method; put a particular story's palette and face proportions in its project profile. Future pages inherit that accepted recipe and are compared to the anchor; renew human review for material departures, not routine unchanged pages. Never label a still-pending candidate as the locked style.
