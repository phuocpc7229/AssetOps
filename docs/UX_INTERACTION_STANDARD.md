# AssetOps UX Interaction Standard

## Intent

AssetOps interactions should feel smooth, fast, and controlled. Motion exists to clarify state changes, confirm user intent, and reduce abrupt page changes without changing the approved enterprise IT visual identity.

## Timing

- Micro feedback: `120-140ms` for button press, icon color, and small state changes.
- Standard feedback: `160-180ms` for hover, focus, dropdowns, form feedback, and table row highlights.
- Larger transitions: `180-220ms` for page, modal, and toast transitions.
- Avoid transitions longer than `220ms` unless explicitly approved.

## Easing

- Default easing: `cubic-bezier(0.2, 0, 0, 1)`.
- Avoid bounce, elastic, spring, or overshoot easing.
- Reduced-motion users must receive minimal or disabled animation.

## Hover Rules

- Hover states may adjust border color, glow intensity, foreground color, or background tint.
- Cards may lift by `1-2px`; tables should not shift layout.
- Disabled controls do not animate beyond opacity changes.
- Hover effects must preserve the current AssetOps color system.

## Focus Rules

- Keyboard focus must be visible with a cyan outline or equivalent focused border/glow.
- Form controls should use border and glow changes, not size changes.
- Validation feedback should appear near the affected field and should not push unrelated layout unexpectedly.

## Modal Behavior

- Modals use a soft overlay fade and a slight upward/scale entrance.
- Modal transitions should complete within `220ms`.
- Closing a modal should be as subtle as opening it.
- Modal content should not bounce, rotate, or use flashy effects.

## Dropdown Behavior

- Dropdowns open with a short fade and slight downward motion.
- Dropdowns should retain their origin and avoid layout jumps.
- Menu item hover states should be clear but restrained.

## Page Transition Rules

- Dashboard pages use a soft fade with slight upward motion.
- Asset list pages use a subtle right-to-left slide/fade.
- Sites and Master Data use soft fade/scale.
- Form pages use a gentle fade.
- Route transitions should stay within `180-220ms`.

## Loading Rules

- Loading text should be direct and specific to the operation.
- Buttons should show the in-progress action, such as `Saving...` or `Updating...`.
- Loading states should not introduce new layout patterns.

## Toast Rules

- Toasts appear in the top-right with a short fade/slide.
- Toast text should confirm the result in one sentence.
- Success, warning, and error colors must use the existing AssetOps palette.

## Reduced Motion

- Respect `prefers-reduced-motion: reduce`.
- Disable or minimize transforms and animation duration for reduced-motion users.
- Preserve state clarity through color, border, and text changes when motion is reduced.
