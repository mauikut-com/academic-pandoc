---
title: "Cimory Sales App — Scale-out Storyboard"
subject: "Horizontal scaling of the Cimory sales app (milk, yogurt, RTE sausages)"
style: "Zack D Films 3D explainer"
aspect: "16:9"
fps: 24
duration: "60–90s"
scenes: 7
---

# Master brief

**Audience.** Business and technology stakeholders who need to understand, in
plain terms, what horizontal scaling means for a sales app and why careless
scale-down hurts real users.

**Tone.** Fast, clean, visual explainer. No jargon dumps — every idea is shown
as a 3D object, a glowing data readout, or a floating caption.

**Context.** Cimory sells dairy (milk, yogurt) and ready-to-eat (RTE) sausages
through a sales app. Under normal load a single app server is enough. A promo
flash sale spikes traffic; scaling **out** (adding servers) restores the
experience, and scaling **down** (removing servers to save cost) degrades it.

**Story arc (7 scenes).** hook → baseline → spike → scale-out → scale-down →
right-sizing → outro. Total 60–90 seconds, ~8–12 seconds per scene.

---

# Style bible

Shared look and feel applied to every scene. Prepend to any standalone scene.

> High-quality 3D animated explainer in the style of Zack D Films. Dark navy
> and charcoal background with soft vignette. Clean, glossy 3D CGI rendering.
> Glowing neon cyan and electric-blue accents throughout; warm orange and red
> reserved only for warnings, overload, and errors. Floating, translucent
> holographic UI panels and data readouts with crisp white text. Soft
> volumetric light rays and subtle depth of field. Smooth, floating camera
> motion with occasional sharp punch-in zooms on key objects. Pop-in white
> caption text synchronized to narration. Stylized 3D products: a white milk
> carton with a blue "Cimory" band, a white yogurt cup, and a red-and-gold
> ready-to-eat sausage pack. A stylized smartphone with a clean Cimory storefront
> UI acts as the recurring "user" object.

## Shared negative prompt

> photorealistic, live action, real human faces, film grain, blurry, low
> detail, jittery or flickering motion, distorted anatomy, extra fingers,
> text artifacts, misspelled words, warped logos, watermark, any logo other
> than Cimory, cluttered composition, harsh flat lighting, washed-out colors,
> inconsistent scale between objects

---

# Scene 1 — Hook

**Goal.** Grab attention and pose the central question.

**Duration.** ~8s

**Shot(s).** Wide shot of a dark void; slow push-in toward a floating phone.

**Prompt.**
A dark navy void with soft volumetric light rays. Three stylized 3D products —
a white milk carton with a blue "Cimory" band, a white yogurt cup, and a
red-and-gold ready-to-eat sausage pack — slowly orbit a large glowing
smartphone floating center-screen. Thin cyan light trails follow the orbit.
The camera pushes in toward the phone screen, which shows a clean Cimory
storefront. A bold white caption pops in with a sharp zoom: "Can your sales app
survive a flash sale?" A faint Cimory logo glows behind the phone. Smooth,
floating camera motion; glossy 3D CGI; dark navy background.

**Negative prompt.**
No products missing from the orbit; no text on the phone screen (keep the UI
clean); no answer yet — do not show servers.

---

# Scene 2 — Baseline

**Goal.** Establish smooth normal operation: one server, sub-second checkout.

**Duration.** ~10s

**Shot(s).** Two-up: server rack on one side, phone on the other; then a
fast tracking shot of the order packet.

**Prompt.**
Interior of a clean 3D data center under calm blue lighting. A single glowing
server rack sits at center-right, its status lights a steady cyan. On the left,
a stylized smartphone shows the Cimory storefront with a milk carton, a yogurt
cup, and a sausage pack. A finger taps "Order"; a glowing cyan packet shoots
along a light line to the server rack and returns. A green checkmark pops over
the phone, and a holographic readout reads "Order placed — 0.8 s". Soft
volumetric light, glossy 3D CGI, dark navy background, floating holographic UI,
smooth camera.

**Negative prompt.**
No red or orange lights; no queue; no other servers — exactly one rack.

---

# Scene 3 — Spike

**Goal.** Show a traffic surge overwhelming the single server.

**Duration.** ~10s

**Shot(s).** Countdown UI, then a flood of avatars; close-up on the rack
overheating.

**Prompt.**
A holographic flash-sale countdown ticks "3 … 2 … 1", then thousands of tiny
glowing user avatars flood toward a single server rack. The rack begins to
glow red and orange, emits a heat shimmer, and its status lights flicker.
Yellow warning triangles pop in. Glowing order packets pile into a growing
queue in front of the rack. A holographic latency readout climbs rapidly.
Dramatic warm lighting against the dark navy background, sharp punch-in on the
overloaded rack, glossy 3D CGI, floating holographic UI.

**Negative prompt.**
No additional servers appear; the queue does not drain; no green recovery
indicators.

---

# Scene 4 — Scale-out

**Goal.** Show horizontal scaling restoring performance.

**Duration.** ~12s

**Shot(s).** Load balancer appears; rack clones 1→2→4→8; parallel traffic lanes.

**Prompt.**
The same 3D data center. A glowing translucent load balancer appears in front
of the overloaded rack. The single rack clones into two, then four, then eight
glowing server racks arranged in a neat row. Traffic splits into parallel cyan
lanes, each feeding a different rack. The queue drains quickly. Status lights
turn a steady green and a holographic latency readout drops back down. A caption
pops in: "Scale out: add servers." Glossy 3D CGI, dark navy background, glowing
neon cyan accents, smooth camera, floating holographic UI.

**Negative prompt.**
No removal of servers; no red or orange lights; do not imply vertical scaling
(no single machine growing larger).

---

# Scene 5 — Scale-down (cost-cut → degraded UX in minutes)

**Goal.** Illustrate that scaling down server capacity trickles down to the
end-user experience, worsening over a span of minutes.

**Duration.** ~14s

**Shot(s).** Racks power off one by one; cut to a customer phone showing a
checkout spinner; a timer climbs across minutes; avatars abandon carts.

**Prompt.**
The eight glowing server racks switch off one by one to cut cost: each rack's
lights fade, the cabinet dims, and it retracts into the dark background, until
only one rack remains — now glowing red and overloaded. Cut to a stylized
smartphone held by a customer avatar, showing the Cimory checkout screen with a
spinning loader. A holographic timer readout above the phone climbs in real
time: "1 minute … 3 minutes … 5 minutes …", then flashes "timeout". Neighboring
customer avatars show red exclamation marks and their carts fade away as they
abandon the purchase. A bold caption pops in: "Scale down, and the slowdown
trickles down to every user — in minutes." Moody warm-red lighting, dark navy
background, glossy 3D CGI, floating holographic UI, slow push-in on the spinner.

**Negative prompt.**
No new servers appearing; no recovery or green indicators; no sudden jump —
the degradation must read as gradual and time-based (minutes); no real human
faces.

---

# Scene 6 — Right-sizing / autoscaling

**Goal.** Present the answer: capacity should follow demand automatically.

**Duration.** ~10s

**Shot(s).** A central gauge and an autoscaler adjusting racks to a demand curve.

**Prompt.**
A central glowing gauge with a smooth demand curve running across it. A smart
autoscaler — a glowing control node — adds and removes glowing server racks in
sync with the curve: racks spawn when the curve rises and fade out when it
falls. The rack count stays balanced, status lights remain a calm cyan-green,
and a latency line holds flat. A caption pops in: "Autoscale: capacity follows
demand." Dark navy background, glossy 3D CGI, neon cyan accents, floating
holographic UI, smooth camera.

**Negative prompt.**
No overload, no red or orange lights, no abrupt jumps, no real dashboards with
readable text beyond the captions.

---

# Scene 7 — Outro

**Goal.** Resolve the story and land the brand.

**Duration.** ~8s

**Shot(s).** Front-on settle shot of the phone and products; logo and tagline.

**Prompt.**
The Cimory storefront smartphone sits front and center with a steady green
status light, healthy and responsive. The three stylized products — milk
carton, yogurt cup, and RTE sausage pack — settle neatly beside it. The Cimory
logo fades in above, and a final caption reads: "Scale smart. Keep every order
fast." Lighting cools to a calm cyan, camera settles to a stop, soft volumetric
glow, glossy 3D CGI, dark navy background.

**Negative prompt.**
No red or orange indicators; no cluttered UI; no extra products or competing
logos.
