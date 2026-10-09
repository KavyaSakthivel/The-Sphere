# Evolve for Her → Sphere: brand and visual analysis

Reviewed 8 October 2026. This is a design interpretation of the public website,
not access to Evolve's internal strategy or evidence of its conversion performance.
The brief is to carry its premium feeling into Sphere in a cooler palette.

## Research scope

Read and visually inspected the live [homepage](https://evolveforher.com/),
[Our Story](https://evolveforher.com/pages/our-story),
[Our Space](https://evolveforher.com/pages/our-space),
[Wellness](https://evolveforher.com/pages/wellness-offerings),
[Annual Membership](https://evolveforher.com/pages/membership-annual), and
[Community](https://evolveforher.com/pages/community-events). Inspected the desktop
hero, navigation, interior gallery, wellness selection, membership details and
community photography. Read the hierarchy and computed typography in the browser.

## What creates the premium impression

| Observed design choice | Interpretation | Application to Sphere |
| --- | --- | --- |
| Large, closely framed human imagery before practical detail | Visitors encounter a feeling and an identity before a product list | Keep Sphere's genuine footage immersive; let the new circle photograph demonstrate intimacy |
| Coordinated timber, stone and clay in the photography | Repetition of material tones creates a coherent world | Use a consistent petrol, pearl and mineral family around Sphere's actual studio photography |
| White navigation and a centred wordmark against imagery | The identity stays quiet while the image carries the mood | Retain the original ivory logo; use deep teal behind navigation for predictable readability |
| A restrained sans serif in navigation and most content | Legibility and consistency support an assured presentation | Keep Sphere's brand sans serif, normal weights and a controlled heading hierarchy |
| Widely spaced photographic sections and simple page structure | A small number of deliberate elements communicate curation | Preserve generous margins; reduce redundant blank padding and use contrast to signal changes in purpose |
| Wellness grouped into a small set of categories | A broad offering becomes easier to understand | Keep Sphere's five clear experience tabs and photographic detail pages |
| Story language centred on care and belonging | Recognition of the whole woman is more personal than performance language | Preserve Sphere's own voice about the woman beyond her roles and the space to simply be |
| Community shown through human proximity and shared activity | Connection becomes visible rather than an abstract claim | Use the requested meditation-circle photograph at the invitation moment |
| Membership details collected in a visibly bounded surface | Practical information is separated from the emotional opening | Keep joining details structured; distinguish the reader's note as personal correspondence |
| Named partners and practitioners on the story page | Specific people can make expertise more tangible | Sphere should add verified people and credentials when supplied; the design cannot manufacture them |

The most useful lesson is coherence: imagery, language, typography and the route
to membership reinforce the same promise. Copying warm brown surfaces alone would
not recreate that effect. Sphere's promise is a small, thoughtful community;
the treatment should feel composed, personal and private while remaining welcoming.

## Cool color direction now applied

| Color | Hex | Purpose |
| --- | --- | --- |
| Petrol teal | #123E46 | Navigation, headings, membership invitation, primary actions |
| Deep teal | #082C33 | Footer, hover states and visual depth |
| Pearl | #F6F8F6 | Main reading surface |
| Mineral mist | #E1EBEB | Community and supporting sections |
| Letter backdrop | #D6E3E5 | Separates the personal note from membership |
| Letter paper | #F9FAF6 | Opaque, framed correspondence surface |

The original supplied ivory and sage logo artwork remains unchanged. The deep
primary shifts from green toward blue, making the design visibly cooler. Pale
surfaces are neutral enough to let skin tones and natural materials remain real.
Strong light/dark contrast supplies richness; a small connected family supplies
restraint. The letter uses a serif italic quotation as a deliberate change of
voice, a thin dividing rule, readable teal prose and the existing handwritten
signature. This signals a message addressed to the reader rather than another
membership sales section.

## Psychology: what can and cannot be concluded

The intended associations are composure, considered care, privacy and belonging.
These are interpretations of this particular combination, not universal effects
of teal or predictions about every affluent visitor. Color varies in hue,
lightness and saturation; reducing the analysis to one named hue is insufficient.
[Labrecque and Milne's marketing study](https://link.springer.com/article/10.1007/s11747-010-0245-y)
supports a relationship between color and perceived brand personality.
[Elliot's review](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full)
emphasizes the role of context and the limits of practical generalization.

Here the design uses contrast and repetition as visible design mechanisms:
consistent colors reduce competing signals; actual group imagery substantiates
the community promise; clear choices reduce the work of exploring the club; and
a distinct letter surface marks a change from practical detail to personal voice.
No clinical efficacy or luxury facilities from the reference are attributed to
Sphere. No reference photography, logo or copy is used in the Sphere website.

## Implementation and review

Source styling: `templates/luxury.css`, with the corresponding cool adjustments
in `templates/event/event.css`. The invitation photo and letter structure live in
`templates/premium-main.html`. Both the homepage and Membership share the requested
circle photograph. The letter is on Membership, where the full original message
remains intact. The source assets and page copy remain authentic to Sphere.

Responsive verification includes the homepage, Membership, Our Story,
Experiences, Journal articles and Carnival, plus the invitation dialog and
experience selector. Content, SEO and montage validation scripts remain required
after building. Changes are local; no production deployment is implied.

### Completed verification

Content, SEO and montage scripts passed. Home, Membership, Experiences, Our
Story, a Journal article and Carnival were checked at 320px and 1440px with no
horizontal overflow. The letter was visually inspected at desktop, 390px and
320px. The invitation dialog opens correctly on mobile. The requested photo is
exported from the original 7008 × 4672 DSC09844.ARW downloaded from the shared
Drive folder. The complete group composition appears in the invitation section;
no screenshot interface remains. Saved desktop review images are
`notes/sphere-cool-intimate-desktop.png` and `notes/sphere-cool-note-desktop.png`.
