/**
 * main.ts — an example Minefort Citadel pack in TypeScript.
 *
 * It exercises every calling convention of the Citadel API so the emitted
 * Luau can be checked against the documented forms:
 *   - dot calls:   world.fill(...), world.time(...), task.spawn(...)
 *   - colon calls: player.message(...), conn.cancel(), block.notify()
 *   - callable tables: vec3(...), color(...)
 *   - multi-returns: const [a, b] = world.light_at(...) / camera.path(...)
 *   - spec literals: game.blocks.define({ ... }) with optional callback fields
 */

const SPAWN = vec3(0.5, 65, 0.5);

// ---------------------------------------------------------------- dot calls
// A welcome platform at spawn (world.* are dot calls).
world.fill(SPAWN, vec3(8, 65, 8), "smooth_stone");

// Overloads from the docs: hold the sky at a named time, then read ticks.
world.time("noon");
const ticks: number = world.time();

// Multi-return: the sky and block light at spawn.
const [skyLight, blockLight] = world.light_at(SPAWN);

// ------------------------------------------------------------- custom blocks
// A spec literal: every field but `name` is optional; callbacks are arrow
// functions (they are stored as plain fields — never `self`-calling).
game.blocks.define({
    name: "pack:beacon",
    looks: "sea_lantern",
    on_tick: (block) => {
        block.notify();
    },
});

// ------------------------------------------------------------------ players
// Subscriptions return a Connection; cancel() is a colon call.
const clickConn = players.on_click((player, hit) => {
    const at = hit.block ?? SPAWN;
    player.message(`clicked ${hit.button} at ${at.x}, ${at.y}, ${at.z}`);
});

players.on_join((player) => {
    // colon call + named colour for the text
    player.message("Welcome to the citadel", colors.gold);
    player.give("torch");
});

clickConn.cancel();

// ------------------------------------------------------------------ helpers
// A one-shot timer: task.* are dot calls; task.wait yields the thread.
task.spawn(() => {
    task.wait(5);
    message("five seconds in — the beacon is running", colors.gold);
});

// A camera fly-by: camera.path returns (camera, runner) as a multi-return.
const [cam, run] = camera.path([
    { at: vec3(0, 90, 40), look_at: SPAWN },
    { at: SPAWN, duration: 4, easing: "out" },
], { easing: "in_out" });

// A tween: any live field eased over time (returns an opaque handle).
const rise = tween(SPAWN, { y: 70 }, { duration: 3, easing: "in_out" });

// The engine's own log — dot call with variadic args.
citadel.log("pack ready at tick", ticks, "light", skyLight, blockLight, cam, rise);
