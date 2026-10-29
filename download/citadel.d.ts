/**
 * citadel.d.ts — TypeScript declarations for the Minefort Citadel Luau API.
 *
 * GENERATED from the official Minefort Citadel documentation (the crawled
 * corpus in scripts/dataset.json — every documented API member) — regenerate
 * with:  python3 scripts/gen_citadel_dts.py
 * Do not edit by hand.
 *
 * Sourcing rules (strictly no invention):
 *   - every interface, function and field below is converted mechanically
 *     from the documented signatures in dataset.json;
 *   - the few members the reference section lacks (task.*, camera.path,
 *     Vec3/Color shapes, player.ui) come from the wiki pages built from the
 *     same official docs, and carry a "Source:" comment;
 *   - anything the docs leave unspecified is typed `unknown`.
 *
 * Calling conventions (TypeScriptToLua): members with `this: void` are dot
 * calls (world.spawn(...)); members without it are Lua colon calls
 * (player:message(...), connection:cancel()). Callbacks are always
 * `this: void` — pass arrow functions. Multi-value returns use
 * LuaMultiReturn: destructure with `const [a, b] = ...`.
 */

// Luau `buffer` — an opaque byte buffer (the docs never enumerate members).
type buffer = unknown;

/** Citadel's DataView — a live view over persistent data, readable and
 *  writable by any key (the documented typedef is `{ [any]: any }`). NB:
 *  unrelated to the ECMAScript DataView that comes with lib esnext; the
 *  two declarations merge, but only the index below is Citadel's. */
interface DataView {
    [key: string]: any;
}

// ================================ Globals ================================
// ===========================================================================
// VERIFIED SUPPLEMENT — members the reference section does not carry, taken
// from the wiki pages built from the official docs. Each block cites source.
// ===========================================================================

/** A position or direction: `vec3(x, y, z)`.
 *  Source: wiki Conventions ("Positions are vec3(x, y, z) with fields
 *  x, y, z"); methods from the "Vectors and colours" doc. Method names and
 *  arities are documented; return types follow the standard vector
 *  semantics, with lerp corroborated by the documented Color.lerp
 *  signature. The documented operators (+ - * / unary - ==) are not
 *  representable in TypeScript and are not declared. */
interface Vec3 {
    x: number;
    y: number;
    z: number;
    /** `a:magnitude()` */
    magnitude(): number;
    /** `a:unit()` */
    unit(): Vec3;
    /** `a:dot(b)` */
    dot(other: Vec3): number;
    /** `a:cross(b)` */
    cross(other: Vec3): Vec3;
    /** `a:distance(b)` */
    distance(other: Vec3): number;
    /** `a:lerp(b, t)` */
    lerp(other: Vec3, t: number): Vec3;
    /** `a:floor()` */
    floor(): Vec3;
    /** `a:with{ y = 70 }` — a copy with the given fields replaced. */
    with(fields: { x?: number; y?: number; z?: number }): Vec3;
}

/** Callable global `vec3`: the constructor (dataset typedef) plus the
 *  dataset members `vec3.up` and `vec3.zero`. */
interface Vec3Constructor {
    (this: void, x: number, y: number, z: number): Vec3;
    up: Vec3;
    zero: Vec3;
}
declare const vec3: Vec3Constructor;

/** A colour: fields `r`, `g`, `b` in 0..1. Source: wiki Conventions
 *  ("Colours are color(r, g, b) in 0..1"); lerp from the documented
 *  `lerp: (self: Color, other: Color, t: number) -> Color` signature. */
interface Color {
    r: number;
    g: number;
    b: number;
    /** `c:lerp(d, t)` */
    lerp(other: Color, t: number): Color;
}

/** Callable global `color`: `color(r, g, b)` (dataset typedef), plus its dataset members. */
interface ColorConstructor {
    (this: void, r: number, g: number, b: number): Color;
        /** The colour `u` (0 to 1) of the way along the list; with `loop`, `u` wraps and the last colour runs back into the first. */
gradient(this: void, list: Ink[], u: number, loop?: boolean): Color
        /** Makes a colour from hue, saturation and value, each 0 to 1. */
hsv(this: void, h: number, s: number, v: number): Color
        /** The colour a picture really shows, since it snaps to the map palette. */
nearest(this: void, c: Color): Color
}
declare const color: ColorConstructor;

/** message — callable global. Sends a chat line to everyone in the main room; `color` is for the words that did not pick one. */
declare function message(this: void, text: Text, color?: Ink): void;

/** tween — callable global. Any live field eased over time: numbers, vec3 and color values tween; a table field is replaced when it lands. */
declare function tween(this: void, target: any, to: { [key: string]: any }, opts?: { duration?: number; easing?: Easing; on_done?: (this: void) => void }): Tween;

// A named time of day. RECOVERED verbatim from the documented leads —
// TimeName: "sunrise, day, noon, sunset, night or midnight" and world.time:
// "ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"".
// (The dataset's TimeName typedef string is extract-damaged.)
type TimeName = "sunrise" | "day" | "noon" | "sunset" | "night" | "midnight";

/** The face-keyed texture table a BlockSpec takes. RECOVERED from the
 *  documented Faces leads + their flattened signatures: `all` is one
 *  picture for all six faces, `side` for the four sides, `top` and
 *  `bottom` the ends (Faces.all); the six direction names with a face
 *  left out defaulting to `side` (Faces.down); `front`/`back` for a
 *  facing block (Faces.front). */
type Faces =
    | { all?: TextureRef; side?: TextureRef; top?: TextureRef; bottom?: TextureRef }
    | { up?: TextureRef; down?: TextureRef; north?: TextureRef; south?: TextureRef; west?: TextureRef; east?: TextureRef }
    | { front?: TextureRef; back?: TextureRef };

// `task` — the scheduler. Source: wiki Runtime (the task semantics table)
// and "Modules and tasks": spawn/delay/defer accept a function or a suspended
// coroutine, forward all arguments (including nils) and return that
// coroutine. The thread itself is opaque (no members documented).
interface TaskApi {
    /** `task.spawn(fn, ...)` — runs immediately until the task yields or
     *  returns. Also accepts a suspended coroutine. Returns the thread. */
    spawn(this: void, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.delay(sec, fn, ...)` — after sec elapsed real seconds. */
    delay(this: void, sec: number, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.defer(fn, ...)` — on the next scheduler turn. */
    defer(this: void, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.wait(sec)` — yields the calling thread until sec real seconds
     *  have passed. Event callbacks and main.luau may call it; synchronous
     *  ask handlers and module top levels may not. */
    wait(this: void, sec: number): unknown;
    /** `task.cancel(task)` — works on a suspended task, also after
     *  task.wait; cancelling a running thread is an error. */
    cancel(this: void, task: unknown): void;
}
declare const task: TaskApi;

/** One shot of a camera path. Source: wiki Movement ("Camera paths"):
 *  `{ at = vec3(...), look_at = vec3(...), duration = 5, easing = "out" }`;
 *  `at` may be a player ("a shot { at = player } is the player's eyes").
 *  The docs also note "a player or thing in a shot is read when the shot
 *  starts" — things (mount targets) are accepted but not enumerated. */
interface CameraPathShot {
    at: Vec3 | Player;
    look_at?: Vec3 | Player;
    duration?: number;
    easing?: Easing;
}

/** Source: wiki Movement: `camera.path(shots, { easing = "in_out",
 *  on_done = function() ... end })`. */
interface CameraPathOptions {
    easing?: Easing;
    on_done?: (this: void) => void;
}

/** "It returns the camera and a handle with cancel()" — wiki Movement.
 *  Declared with Lua method-call (colon) convention, like Connection. */
interface CameraPathRunner {
    cancel(): void;
}

/** `camera` — Source: wiki Movement ("Camera paths"): camera.path is a
 *  fixed camera that eases from shot to shot; each shot after the first
 *  takes its own duration (or the path's, 5 seconds by default). */
interface CameraApi {
    path(this: void, shots: CameraPathShot[], opts?: CameraPathOptions): LuaMultiReturn<[Camera, CameraPathRunner]>;
}
declare const camera: CameraApi;

/** The engine itself: the log, the engine and game versions, the environment, and this pack's tick budget. */
interface Citadel {
        /** This pack's slice of a tick, and what it did with it. */
    budget(this: void): Budget
        /** "development", "unlisted" or "published": which copy of the game this is. */
    env: string
        /** The game version from citadel.yml, e.g. */
    game: string
        /** Writes its arguments to the server log, under this pack's name. */
    log(this: void, ...args: any[]): void
        /** Called when a batch runs out of budget; at most once a second. */
    on_slow(this: void, fn: (this: void, slow: Slow) => void): Connection
        /** The engine version, e.g. */
    version: string
}
/** The `citadel` global. */
declare const citadel: Citadel;

/** Every `ColorName` as a value; any other name is an error naming the nearest ("grey" says "gray"). */
interface Colors {
    aqua: Color
    black: Color
    blue: Color
    cyan: Color
    dark_aqua: Color
    dark_blue: Color
    dark_gray: Color
    dark_green: Color
    dark_purple: Color
    dark_red: Color
    gold: Color
    gray: Color
    green: Color
    light_purple: Color
    lime: Color
    magenta: Color
    orange: Color
    pink: Color
    purple: Color
    red: Color
    transparent: Color
    white: Color
    yellow: Color
}
/** The `colors` global. */
declare const colors: Colors;

/** Adds a room's slash commands from a usage line: the `commands` global, or `room.commands`. */
interface Commands {
        /** usage: "bet <amount:integer 1..10000> [color:red|black]". */
    add(this: void, usage: string, fn?: (this: void, player: Player, args: { [key: string]: any }) => string, opts?: CommandOpts): Command
        /** Runs a pack's command for player as if they typed it ("/servers"), with their permissions. */
    run(this: void, player: Player, line: string): boolean
}
/** The `commands` global. */
declare const commands: Commands;

/** Helpers for persistent data views. Player.data remains an ordinary Lua table. */
interface Data {
        /** A detached JSON snapshot as ordinary Lua values/tables. */
    copy(this: void, value: any): any
        /** Insert into a nested data list; omitted index appends. */
    insert(this: void, list: DataView, value: any): void
        /** Insert into a nested data list; omitted index appends. */
    insert(this: void, list: DataView, index: number, value: any): void
        /** Remove and return a detached value; omitted index removes the last element. */
    remove(this: void, list: DataView, index?: number): any
}
/** The `data` global. */
declare const data: Data;

/** Recipes for numbers over the world, for `world.generate`. */
interface Fields {
        /** A scattered grid, one point per `size` blocks: the distance to the nearest point, and that point's own number 0..1. */
    cells(this: void, size: number, seed?: number): { distance: Field; random: Field }
        /** Blocks under the surface: `fields.height - fields.y`. */
    depth: Field
        /** One number 0..1 for each square of `cell` blocks (1). */
    hash(this: void, cell?: number, seed?: number): Field
        /** The y of the surface of a column, as a block. */
    height: Field
        /** `a` where `t` is 0, `b` where it is 1. */
    mix(this: void, a: Field | number, b: Field | number, t: Field | number): Field
        /** Smooth noise, about -1..1. */
    noise(this: void, opts?: { seed?: number; scale?: number; octaves?: number; gain?: number; lacunarity?: number; solid?: boolean }): Field
        /** The height of the open space a block is in: 0 in rock, 64 at most (and in the open sky). */
    room: Field
        /** 1 on a column at the water's edge with water beside it. */
    shore: Field
        /** The step to the steepest of the four columns beside this one. */
    slope: Field
        /** How deep the water is over the surface; 0 and below on land. */
    water: Field
    x: Field
    y: Field
    z: Field
}
/** The `fields` global. */
declare const fields: Fields;

/** Particles for a room: Minecraft's particle packet; the `fx` global, or `room.fx`. */
interface Fx {
        /** Shows particle `name` ("dust", "end_rod", "explosion", "firework", "flame", "note", "totem_of_undying") at `pos`, or at every point of a list. */
    particle(this: void, name: string, pos: Vec3 | Vec3[], opts?: { count?: number; spread?: number | Vec3; velocity?: Vec3; speed?: number; color?: Ink; size?: number }): void
}
/** The `fx` global. */
declare const fx: Fx;

/** The game version a room runs, its entity kinds, blocks and items, and the pack's own blocks, items and recipes: the `game` global, or `room.game`. */
interface Game {
        /** Biomes of the pack's own: a vanilla biome with other colours and weather. */
    biomes: Biomes
        /** Returns one block in this version's numbers, or nil for a name this game has no word for. */
    block(this: void, name: string): Block | undefined
        /** The one table that *adds* to a version rather than reading it. */
    blocks: Blocks
        /** The kinds of entity: `define` a pack's own, `amend` the game's own, and read a kind of the game: a mob kind by either spelling (`game.entities.cow`, `game.entities.Cow`), a kind that is not a mob by its name (`game.entities.arrow`); nil where the game has none. */
    entities: Entities & { [key: string]: EntityKind | EntityDef | undefined }
        /** Returns an item this game has, or nil for a name it does not; never an error. */
    item(this: void, name: string): Item | undefined
        /** Defines items of the pack's own, with a texture for clients from 1.21.4. */
    items: Items
        /** What a crafting grid and a furnace make of a pack's items; recipes are added while the pack loads. */
    recipes: Recipes
        /** The y of this world's sea level. */
    sea_level: number
        /** What this world's overworld is made of: `snow` and `steps`, as citadel.yml writes them; read-only, nil when there is no list. */
    terrain?: { snow?: boolean; steps?: TerrainStep[] }
        /** Returns a new texture of width by height pixels, see-through until drawn on, for a pack's block or item. */
    texture(this: void, width: number, height: number): Texture
        /** This game's version, such as "a0.1.0". */
    version: string
        /** How tall the world is in blocks: 128, or 256 for a 1.8.9 world. */
    world_height: number
}
/** The `game` global. */
declare const game: Game;

/** Fetches public URLs. The call waits like `task.wait`. */
interface Http {
        /** GET a URL. */
    get(this: void, url: string, options?: { query?: { [key: string]: string }; headers?: { [key: string]: string }; timeout?: number; cache?: number }): HttpResponse
        /** Opens a WebSocket (`ws` or `wss`) and keeps it open: when the connection ends, the engine dials again. */
    socket(this: void, url: string, options: { headers?: { [key: string]: string }; on_message: (this: void, message: SocketMessage) => void }): Socket
}
/** The `http` global. */
declare const http: Http;

/** What Minefort tells its own hub: never the servers or the hubs, which it browses with network.browse. Empty lists on every other server. The first call of experiences waits up to two seconds for Minefort's list. */
interface Hub {
        /** The portals of the experience grounds. */
    experiences(this: void): ({ slot: number; experience: string; title: string; pitch?: string; icon?: string; banner?: string; players?: number })[]
        /** Turns the player's own live portal to another published experience. */
    point(this: void, player: Player | string, slot: number, experience: string): boolean
        /** Offers portal `slot` for Gems, to lead to `experience` (what `/play` takes). */
    rent(this: void, player: Player | string, slot: number, product: string, experience?: string): string | undefined
}
/** The `hub` global. */
declare const hub: Hub;

/** The models this pack makes. They go into the resource pack a client is handed when it joins, so `new` belongs at the top of the script: calling it from a callback is an error. */
interface Models {
        /** Makes a model named `name` from the parts `fn` builds and returns it. */
    "new"(this: void, name: string, fn: (this: void, m: ModelBuild) => void): Model
}
/** The `models` global. */
declare const models: Models;

/** An experience made of more than one server: asks for instances of its members and is told about them. A failed call answers nil and a reason. Calls yield, but for `status`. Without a network every answer is no. */
interface Network {
        /** The platform's hub finding every network, in the order to show them. */
    browse(this: void, view: "search" | "for-you" | "recent" | "featured", options?: { player?: Player | string; query?: string; page?: number; category?: string; online?: boolean; ids?: string[]; sort?: "players" | "name"; also?: { recent?: boolean; favorites?: string[] } }): LuaMultiReturn<[BrowseEntry[] | undefined, number | string | undefined, { recent: { rows: BrowseEntry[]; total: number } | false | undefined; favorites: { rows: BrowseEntry[]; total: number } | false | undefined } | undefined]>
        /** The instance to send `players` players to (1 unless set), or nil when none has room. */
    find(this: void, options: { label: string; players?: number; party?: Player | string; start?: { member: string; slots: number; data: any } }): LuaMultiReturn<[NetworkStarted | undefined, string | undefined]>
        /** This server's network, by name, and the instance this pack runs on: `id` and the fields after it are nil on a server that is not one. */
    info(this: void): LuaMultiReturn<[{ network: string; id?: string; member?: string; label?: string; slots?: number; data: any } | undefined, string | undefined]>
        /** Everything this network runs: this experience's own always-on servers (on the platform's hub, the hubs), then its games started on demand. */
    instances(this: void, label?: string): LuaMultiReturn<[BrowseEntry | NetworkInstance[] | undefined, string | undefined]>
        /** Called when an instance's state, open, status or meta changes. */
    on_instance_change(this: void, handler: (this: void, instance: NetworkInstance) => void): Connection
        /** Called when an instance is first seen: started, or already running. */
    on_instance_start(this: void, handler: (this: void, instance: NetworkInstance) => void): Connection
        /** Called with the id of an instance that is gone. */
    on_instance_stop(this: void, handler: (this: void, id: string) => void): Connection
        /** How many play on this network (everyone on Minefort on the platform's hub), or in one mode's games. */
    online(this: void, label?: string): LuaMultiReturn<[number | undefined, string | undefined]>
        /** Starts an instance of `member`. */
    start(this: void, options: { member: string; label: string; slots: number; data: any }): LuaMultiReturn<[NetworkStarted | undefined, string | undefined]>
        /** Says where this instance is. */
    status(this: void, options: { open: number; status?: string; meta: any }): void
        /** Stops an instance of this network. */
    stop(this: void, id: string): LuaMultiReturn<[boolean, string | undefined]>
}
/** The `network` global. */
declare const network: Network;

/** Smooth random numbers for a generator, made by the engine. */
interface NoiseApi {
        /** Returns a noise. */
    "new"(this: void, opts?: { seed?: number; scale?: number; octaves?: number; gain?: number; lacunarity?: number }): Noise
}
/** The `noise` global. */
declare const noise: NoiseApi;

/** Declares named parts of a stored world and the generators that build them; nothing runs on load. */
interface Parts {
        /** Declares a named part and its generator; nothing runs on load. */
    define(this: void, def: PartDefinition): void
}
/** The `parts` global. */
declare const parts: Parts;

/** A room's players and their events: the `players` global, or `room.players`. */
interface Players {
        /** Returns how many players are in the room. */
    count(this: void): number
        /** Returns the player with this name, or nil. */
    get(this: void, name: string): Player | undefined
        /** Returns every player in the room. */
    list(this: void): Player[]
        /** Who is within a radius of a point, and who is inside a box of blocks. */
    near(this: void, pos: Vec3, radius: number): Player[]
        /** Cancellable. */
    on_break(this: void, fn?: (this: void, player: Player, pos: Vec3, block: string) => boolean): Connection
        /** Return false and the line is not said. */
    on_chat(this: void, fn?: (this: void, player: Player, text: string) => boolean): Connection
        /** Calls `fn` on a left or right click; `hit` holds the button and the entity, player, block and face it met. */
    on_click(this: void, fn: (this: void, player: Player, hit: Hit) => void): Connection
        /** Asks `fn` before damage lands on a player; return false to refuse it. */
    on_damage(this: void, fn?: (this: void, player: Player, hit: DamageHit) => boolean): Connection
        /** Calls `fn` when a player dies, with the cause (fall, drown, void, lava, ...) and the line broadcast; `player` is nil once they have left. */
    on_death(this: void, fn: (this: void, player: Player | undefined, cause: string, message: string, by: Player) => void): Connection
        /** Calls `fn` when a stack lands on the ground; `player` is nil where the world dropped it or they have left. */
    on_drop(this: void, fn: (this: void, player: Player, item: string, count: number) => void): Connection
        /** Calls `fn` when a player arrives: on the globals when a client connects, on a room's table each time a player moves into it. */
    on_join(this: void, fn: (this: void, player: Player) => void): Connection
        /** The same player value on_join had; it can no longer be sent to. */
    on_leave(this: void, fn: (this: void, player: Player) => void): Connection
        /** A stack taken off the ground, and one that landed on it. */
    on_pickup(this: void, fn: (this: void, player: Player, item: string, count: number) => void): Connection
        /** Asks `fn` before a player puts a block down; return false to cancel it. */
    on_place(this: void, fn?: (this: void, player: Player, pos: Vec3, block: string) => boolean): Connection
        /** Calls `fn` when a player respawns; `player` is nil once they have left. */
    on_respawn(this: void, fn: (this: void, player: Player) => void): Connection
        /** Calls `fn` when a player picks a hotbar slot, 1..9. */
    on_slot(this: void, fn: (this: void, player: Player, slot: number) => void): Connection
        /** Calls `fn` once per sneak press and release; `down` is true on the press. */
    on_sneak(this: void, fn: (this: void, player: Player, down: boolean) => void): Connection
        /** Returns every player inside a box of blocks, corners included. */
    within(this: void, from: Vec3, to: Vec3): Player[]
}
/** The `players` global. */
declare const players: Players;

/** The main room and new isolated rooms with their own chunks, players and effects. */
interface Rooms {
        /** Creates an isolated room with its own chunks, players and effects; `spawn_point` defaults to (0.5, 65, 0.5), `generate` fills each chunk. */
    create(this: void, opts: { spawn_point?: Vec3; generate?: (this: void, chunk: Chunk) => void }): Room
        /** The main room, whose tables are the globals `world`, `players`, `ui` and the rest. */
    main: Room
}
/** The `rooms` global. */
declare const rooms: Rooms;

/** How players get between the worlds of the group. */
interface Routes {
        /** From one dimension to another: standing `ticks` ticks in `block`, or only by `player:travel` without a trigger; arriving at `placement` or the destination's spawn. */
    add(this: void, route: { from: string; to: string; trigger?: { block: string; ticks?: number }; placement?: Vec3 }): void
}
/** The `routes` global. */
declare const routes: Routes;

/** Sells this experience's products for Gems. Minefort asks the player in its own dialog; the pack learns only paid or not, never a balance, price or reason. Calls yield. Without the platform's shop every answer is no. */
interface Shop {
        /** Called when the player said no or did not answer. */
    on_declined(this: void, handler: (this: void, purchase: ShopPurchase) => void): Connection
        /** Called once per paid purchase; returning without an error hands it over. */
    on_paid(this: void, handler: (this: void, purchase: ShopPurchase) => void): Connection
        /** Whether the player owns this pass. */
    owns(this: void, player: Player | string, product: string): boolean
        /** Asks Minefort to offer `product` to the player. */
    prompt(this: void, player: Player | string, product: string): string | undefined
}
/** The `shop` global. */
declare const shop: Shop;

/** Plays and stops sounds for everyone in a room: the `sound` global, or `room.sound`. */
interface Sound {
        /** Plays a sound by name to everyone in the room; volume above 1 carries further, pitch 0.5..2.0. */
    play(this: void, name: string, opts?: { at?: Vec3; volume?: number; pitch?: number; category?: string }): void
        /** One sound by name, or every sound, for everyone in the room; 1.13+. */
    stop(this: void, name?: string): void
        /** A live stream (MP3, or an FLV's sound) or a pack's sound file (OGG, MP3, WAV), heard through the mod a screen's stream uses. */
    stream(this: void, opts: { url?: string; file?: string; at?: SoundSpeaker | SoundSpeaker[]; to?: Player | Player[]; distance?: number; loop?: boolean; name?: string }): SoundStream
}
/** The `sound` global. */
declare const sound: Sound;

/** Values a pack keeps between restarts, saved by key in its storage.json. */
interface Storage {
        /** Yields until saved; raises an error on failure. */
    flush(this: void): void
        /** Returns the value saved under `key`, or nil when there is none. */
    get(this: void, key: string): any
        /** Every key, sorted; with a prefix, only those that start with it. */
    keys(this: void, prefix?: string): string[]
        /** Saves a value under `key` in this pack's storage.json; nil forgets it. */
    set(this: void, key: string, value: any): void
        /** Last persistence error and whether there are unsaved changes. */
    status(this: void): { pending: boolean; error?: string }
}
/** The `storage` global. */
declare const storage: Storage;

/** Shared durable storage: the experience's one store, leases and raw queries; calls yield. */
interface Stores {
        /** Lists a player's blobs across all blob stores in this scope, each with its store, key, version and size. */
    blob_list(this: void, owner: string): ({ store: string; key: string; version: number; size: number })[]
        /** Takes a lease on `key` for `holder`, lasting `ttl_ms` milliseconds (up to one hour); returns a fencing token. */
    lease(this: void, key: string, holder: string, ttl_ms: number): number
        /** Returns the experience's one store. */
    open(this: void): DurableStore
        /** Gives up the lease on `key` that `token` holds. */
    release(this: void, key: string, token: number): void
        /** Extends the lease on `key` that `token` holds. */
    renew(this: void, key: string, token: number): void
        /** Sends one raw query to the store and yields until it answers; returns the answer table and any blob bytes. */
    request(this: void, query: { [key: string]: any }, bytes?: string): LuaMultiReturn<[{ [key: string]: any }, string | undefined]>
}
/** The `stores` global. */
declare const stores: Stores;

/** Clocks for a pack: a callback every tick, one every few seconds, and the seconds since the pack started. */
interface Time {
        /** Calls `fn` every `seconds`, precise to 1 ms and never drifting; use it for music. */
    every(this: void, seconds: number, fn: (this: void) => void): Connection
        /** Seconds since the pack started. */
    now(this: void): number
        /** Calls `fn` every tick, 20 times a second, with the tick number; keep it short. */
    on_tick(this: void, fn: (this: void, tick: number) => void): Connection
}
/** The `time` global. */
declare const time: Time;

/** Titles, chat, the action bar, boss bars, the sidebar and the tab list: for everyone in a room (the `ui` global, or `room.ui`), or for one player (`player.ui`, the same calls). "Everyone" below is one player on `player.ui`. */
interface Ui {
        /** Shows a line above the hotbar to everyone in the room. */
    actionbar(this: void, text: Text, color?: Ink): void
        /** Shows a boss bar to everyone in the room and returns its handle; progress 0..1. */
    bossbar(this: void, opts?: { title?: Text; color?: BarColor; progress?: number }): Bar
        /** The pieces of a layout (see "Layouts"). */
    box(this: void, opts: { id?: string; width: number; height: number; color?: Ink; radius?: number }): LayoutNode
    column(this: void, opts: { gap?: number; align?: LayoutAlign; [key: number]: LayoutNode }): LayoutNode
        /** A layout of one child, centred over the hotbar with its bottom edge `margin` pixels above the screen's (40, or 25 when `hide_hud` takes the hearts and the food away). */
    define(this: void, name: string, opts: { anchor?: "bottom"; margin?: number; [key: number]: LayoutNode }): Layout
    image(this: void, opts: { id?: string; image: Texture; color?: Ink }): LayoutNode
        /** What a dialog is made of (see "Dialogs"): row, column, stack, space, text, image, and window, button, tabs, close, badge, dot, progress, divider, card, grid, theme, mix and SCREEN. */
    kit: { [key: string]: any }
        /** Words in the client's own letters, space to `~`. */
    label(this: void, opts: { id?: string; text?: string; width?: number; align?: LayoutAlign; color?: Ink }): LayoutNode
        /** The children are the list part: `ui.row{ gap = 4, a, b }`. */
    row(this: void, opts: { gap?: number; align?: LayoutAlign; [key: number]: LayoutNode }): LayoutNode
        /** Sets the sidebar for everyone in the room; lines run top to bottom and only changed lines are sent. */
    sidebar(this: void, opts?: { title?: Text; lines?: Text[] } | false): void
    stack(this: void, opts: { align?: LayoutAlign; [key: number]: LayoutNode }): LayoutNode
        /** Sets the player list's header and footer for everyone in the room. */
    tab(this: void, opts: { header?: Text; footer?: Text }): void
        /** Shows a title and subtitle to everyone in the room; fades and stay are in seconds. */
    title(this: void, opts: { title?: Text; subtitle?: Text; color?: Ink; fade_in?: number; stay?: number; fade_out?: number }): void
}
/** The `ui` global. */
declare const ui: Ui;

/** A room's blocks, entities, displays, screens and time: the `world` global, or `room.world`. */
interface World {
        /** The block there as the handle a hook gets: reads are live, and what it does lands on the next tick. */
    block(this: void, pos: Vec3): BlockAt | undefined
        /** The same value, written in code instead of read from a file. */
    build(this: void, fn: (this: void, b: Builder) => void, opts?: { detail?: number }): Schematic
        /** Makes a picture of `width` by `height` maps (1 by 1 by default, 16 at most a side) with no frame of its own, for a frame, a hand or a screen. */
    canvas(this: void, opts?: { width?: number; height?: number }): Canvas
        /** A chest's stacks, or nil where the block keeps none. */
    container(this: void, pos: Vec3): Container | undefined
        /** Another world of the server's group, by dimension id or its last part ("dungeon", "minecraft:the_nether"): that world's own `world` table. */
    dimension(this: void, name: string): World
        /** A model stands in the world through the same call as everything else, and is the one kind that hands back something other than a Display. */
    display(this: void, opts: { kind: "model"; model: Model; at?: Vec3; rotation?: Orientation; scale?: number | Vec3; paint?: { [key: string]: Ink }; fallback?: string; seats?: Vec3[]; lead?: boolean }): ModelDisplay
        /** A model stands in the world through the same call as everything else, and is the one kind that hands back something other than a Display. */
    display(this: void, opts: { kind: "item" | "text" | "block" | "frame"; at?: Vec3; rotation?: Orientation; scale?: Vec3 | number; billboard?: Billboard; glow?: Ink | false; item?: ItemSpec; canvas?: Canvas; context?: Context; text?: Text; color?: Ink; background?: Ink | false; line_width?: number; shadow?: boolean; block?: string; facing?: ScreenFacing; invisible?: boolean; glide?: number; lead?: boolean }): Display
        /** A stack on the ground at a block, as a broken block leaves one. */
    drop(this: void, pos: Vec3, item: ItemSpec): void
        /** Live and queued entities, in ascending id. */
    entities(this: void, query?: { near?: Vec3; radius?: number; kind?: string; mob?: boolean }): EntityHandle[]
        /** A blast at a point. */
    explode(this: void, pos: Vec3, power?: number): void
        /** Fills a box of blocks between two corners, live, stored and sent to everyone. */
    fill(this: void, from: Vec3, to: Vec3, block: BlockRef): void
        /** Declares this world: the engine makes each chunk from the rules, on every core, and no script runs for a chunk. */
    generate(this: void, rules: GeneratorRules): Generated
        /** Returns the biome name of the column at `pos`; `nil` where that chunk is not in memory. */
    get_biome(this: void, pos: Vec3): string | undefined
        /** `nil` where that chunk is not in memory: a read never generates. */
    get_block(this: void, pos: Vec3): string | undefined
        /** A box, in x, then z, then y order. */
    get_blocks(this: void, from: Vec3, to: Vec3): string | undefined[]
        /** Makes an invisible box a player can click; `solid` also makes it a wall. */
    hitbox(this: void, opts: { at: Vec3; width?: number; height?: number; depth?: number; solid?: boolean; on_click?: (this: void, player: Player, button: "left" | "right") => void }): Hitbox
        /** The stacks on the ground: `{ id, item, count, at }` rows. */
    items(this: void): GroundItem[]
        /** Sends players light no block makes, 1 to 15 a source; each call replaces the last, `{}` ends it. */
    light(this: void, sources: LightSource[]): void
        /** Block light and sky light, 0 to 15, and whether nothing above holds off the sky. */
    light_at(this: void, pos: Vec3): LuaMultiReturn<[number, number, boolean]>
        /** Places a player-shaped entity every client from 1.8 sees; removed when the script ends or reloads. */
    npc(this: void, opts: { name?: string; at?: Vec3; rotation?: BodyRotation; skin?: string | { value: string; signature: string } | false }): Npc
        /** What the survival tick did. */
    on_block_break(this: void, fn: (this: void, player: Player, pos: Vec3, block: string) => void): Connection
        /** Tells after a block was placed, with its canonical name. */
    on_block_place(this: void, fn: (this: void, player: Player, pos: Vec3, block: string) => void): Connection
        /** Tells after a mob died; it is gone, so its id and name is all there is. */
    on_entity_death(this: void, fn: (this: void, id: number, name: string) => void): Connection
        /** Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. */
    on_entity_spawn(this: void, fn: (this: void, entity: EntityHandle, name: string) => void): Connection
        /** Called for a chunk each time it comes into memory, in a script world; it must make the same blocks every time. */
    on_generate(this: void, fn: (this: void, chunk: Chunk) => void): void
        /** Each chunk the overworld terrain made, once, after it made it. */
    on_populate(this: void, fn: (this: void, chunk: Chunk) => void): void
        /** Live, stored and sent; air is skipped unless `air` is true. */
    paste(this: void, schem: Schematic, origin: Vec3, opts?: { air?: boolean; part?: string }): void
        /** The points a body walks from `from` to the block at `to`, or nil. */
    path(this: void, from: Vec3, to: Vec3, opts?: { size?: number | number[]; swim?: boolean; fall?: number; range?: number; budget?: number }): Vec3[] | undefined
        /** Places a mob's body with no mind of its own that the script moves; its name tag always shows. */
    puppet(this: void, opts: { kind: string; at?: Vec3; rotation?: BodyRotation; name?: Text }): Puppet
        /** The first block a ray from `from` along `direction` meets within `max` blocks, and the face it came in through; nil for none. */
    raycast(this: void, from: Vec3, direction: Vec3, max?: number): RayHit | undefined
        /** `n` lines at once. */
    raycasts(this: void, rays: buffer, out: buffer, n: number): void
        /** `world.rules{ fall = true }` switches one on, false off; a rule left out or nil keeps its value, and a number or a string is an error. */
    rules(this: void, opts?: { survival?: boolean; fall?: boolean; damage?: boolean; hunger?: boolean; anticheat?: boolean; day_cycle?: boolean; redstone?: boolean }): Rules
        /** A file inside the pack; a path that leaves it, or one that is not there, is an error naming the file. */
    schematic(this: void, file: string): Schematic
        /** Puts a wall of map frames, `width` by `height` frames (128 pixels each), in front of a wall; `at` is the top-left frame. */
    screen(this: void, opts: { at: Vec3; facing: Facing | "up"; up?: Facing; width?: number; height?: number; glow?: boolean; on_click?: (this: void, player: Player, x: number, y: number, button: "left" | "right") => void }): Screen
        /** True when no block stops the line from `from` to `to`: a block with a collision box does (glass, leaves), water and grass do not. */
    sees(this: void, from: Vec3, to: Vec3): boolean
        /** `skin` is for "player_head" and "player_wall_head" only: an account's name, or the raw `textures` property. */
    set_block(this: void, pos: Vec3, block: BlockRef, opts?: { skin?: HeadSkin }): void
        /** Sets many blocks at once, live, stored and sent; the cheapest way. */
    set_blocks(this: void, changes: ({ at: Vec3; block: BlockRef; skin?: HeadSkin })[]): void
        /** Puts an entity at a point and returns its handle. */
    spawn(this: void, def: EntityDef | string, pos: Vec3, data?: { [key: string]: any }): EntityHandle | undefined
        /** Where players arrive in this room; writable. */
    spawn_point: Vec3
        /** Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, `s` seconds after the call. */
    time(this: void, at: number | TimeName | ((this: void, s: number) => number)): void
        /** Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, `s` seconds after the call. */
    time(this: void): number
        /** Makes a box of blocks, both corners included, that knows who is in it; checked once a tick by feet position. */
    zone(this: void, opts: { from: Vec3; to: Vec3; on_enter?: (this: void, player: Player) => void; on_leave?: (this: void, player: Player) => void }): Zone
}
/** The `world` global. */
declare const world: World;

// ================================= Types =================================
/** What one kind of ask has cost this pack, and what every kind has together. An ask is a question the engine puts to a pack with a deadline on it; an answer that does not arrive in time is not used. */
interface AskCount {
        /** Answers that arrived in time. */
    answered: number
        /** Questions the engine put to this pack. */
    asks: number
        /** True once the engine has stopped asking this pack this kind at all. */
    disabled: boolean
        /** Answers that arrived after the engine had acted, and were dropped. */
    late: number
        /** Deadlines that passed with no answer. */
    missed: number
        /** Asks never sent, because this kind is switched off for this pack. */
    skipped: number
}

/** What the engine's questions with a deadline have cost this pack, in total and per kind: `citadel.budget().asks`. */
interface Asks {
        /** The same counters per kind of question, e.g. */
    kinds: { [key: string]: AskCount }
}

/** A boss bar, from `ui.bossbar` for the room or `player.ui.bossbar` for one player; title, progress and colour are live. */
interface Bar {
        /** The bar's colour, from its own closed set; anything else is white. */
    color: BarColor
        /** Removes the bar. */
    destroy(): void
        /** How full the bar is, 0 to 1; live. */
    progress: number
        /** Reads back the words; takes any text. */
    title: Text
        /** Whether players see the bar; false takes it off their screens, true or nil shows it again. */
    visible?: boolean
}

/** What a pack changes about the vanilla biome its own biome copies. Each colour is a `Color` or a colour name such as "#7fd8c8". */
interface BiomeDefinition {
        /** The colour of the far distance. */
    fog?: Color | string
    grass?: Color | string
    leaves?: Color | string
        /** The vanilla biome to copy; "plains" when left out. */
    like?: string
        /** Lower case letters, digits and underscores. */
    name: string
    sky?: Color | string
    water?: Color | string
        /** The colour of the view under water. */
    water_fog?: Color | string
    weather?: "rain" | "snow" | "none" | false
}

/** The biomes a pack adds to the game. */
interface Biomes {
        /** Defines a biome, or changes the one of that name, and returns its full name ("mypack:crystal"). */
    define(this: void, def: BiomeDefinition): string
}

/** One block the game version has, in its own numbers, from `game.block(name)`: hardness, light, fire and material. */
interface Block {
        /** The rule Citadel runs for it, such as "grass", "flowing", "torch" or "falling"; nil for a block that does nothing on its own. */
    behaviour?: string
        /** The one field a pack writes. */
    drops?: boolean
        /** Fire's two numbers: how readily it catches and how fast it burns away. */
    flammability?: { catches: number; burns_away: number }
        /** Seconds-scale hardness in this version's numbers; below zero is unbreakable. */
    hardness: number
        /** What it gives off, 0..15, and what a step through it takes away. */
    light: number
        /** What a step through it takes off the light, 0 to 15. */
    light_filter: number
        /** The jar's Material as five questions; nil in a game with no block-update tables. */
    material?: Material
        /** The block's canonical name. */
    name: string
        /** Whether it is an opaque full cube, which is not the material's question. */
    opaque: boolean
        /** Whether the random-tick pass acts on it. */
    random_ticks: boolean
        /** The three the block-update tables own: nil in a game that has none. */
    resistance?: number
}

/** What `game.blocks.amend` takes: **hooks only**.  Every tnt in every world already looks like tnt and is as hard as tnt, so a data column here is refused by name. For a block of your own with different numbers, `game.blocks.define { extends = "tnt" }`. */
interface BlockAmendSpec {
        /** It has just been stored, whatever stored it. */
    on_added?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** Something broke it; `by` says what. */
    on_break?: (this: void, block: BlockAt, player: Player, by: Breaker, base: (this: void, ...args: any[]) => any) => Drops | undefined
        /** A neighbour at `from` changed; `announced` is the block the notifier announced itself as. */
    on_neighbour?: (this: void, block: BlockAt, from: Vec3, announced: string, base: (this: void, ...args: any[]) => any) => void
        /** A player put it down. */
    on_place?: (this: void, block: BlockAt, player: Player, base: (this: void, ...args: any[]) => any) => void
        /** A redstone signal started (`powered` is true) or stopped reaching it. */
    on_power?: (this: void, block: BlockAt, powered: boolean, base: (this: void, ...args: any[]) => any) => void
        /** The random pass landed on it. */
    on_random_tick?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** It has just gone. */
    on_removed?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** A body (a player, mob, item or other) is standing on it. */
    on_step?: (this: void, block: BlockAt, body: Body, base: (this: void, ...args: any[]) => any) => void
        /** A scheduled tick this block asked for came due. */
    on_tick?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** It was lit, blasted or burnt; `cause` is "ignite", "explosion" or "fire". */
    on_trigger?: (this: void, block: BlockAt, cause: Trigger, base: (this: void, ...args: any[]) => any) => void
        /** Somebody right-clicked it; `held` is the item in hand. */
    on_use?: (this: void, block: BlockAt, player: Player | undefined, held: string, base: (this: void, ...args: any[]) => any) => Used | undefined
}

/** The block a hook was called about.  Reads are fields and acts are methods. The reads are **live** — the world as it is right now — and everything that changes the world is carried out by the engine the moment the hook returns, in the order it was asked for. */
interface BlockAt {
        /** The block's position; a live read. */
    at: Vec3
        /** **The door**: this block stops being a block, and that entity appears. */
    become(entity: string, data?: { [key: string]: any }): void
        /** What this block remembers beyond its state; kept with the position, saved with the chunk, and gone when the block goes. */
    data: DataView
        /** Takes it out, leaving nothing. */
    destroy(): void
        /** A name, or an item table: a pack item keeps its id. */
    drop(item: ItemSpec, count?: number): void
        /** A facing block's front: "north", "south", "west", "east"; nil otherwise. */
    facing?: Facing
        /** The block one face away, by name; nil where that chunk is not in memory. */
    get(face: Face): string | undefined
        /** The block's name with its namespace, such as "rave:crate"; a live read. */
    name: string
        /** Tells the six neighbours this block changed. */
    notify(): void
        /** Whether a redstone signal reaches it: what a lamp asks. */
    powered?: boolean
        /** Which room the block is in. */
    room: number
        /** Asks for this block's `on_tick`, `tick_every` seconds from now. */
    schedule(): void
        /** Puts another block at this position. */
    set(block: BlockRef): void
        /** Which of this definition's states it is in, counting from 1. */
    state: number
}

/** The handle `define` hands back. Equality is identity — two handles are the same block when they name the same block. */
interface BlockDef {
        /** The block as an item, when the definition gave it one: `player:give(def.item)`. */
    item?: ItemTable
        /** Canonical, with the pack's namespace already on it: "rave:crate". */
    name: string
        /** How many states it has; `block.state` counts 1 to this. */
    states: number
}

/** `game.blocks`: defines a pack's own blocks and amends the game's own, at load time. */
interface Blocks {
        /** Only the game's own blocks, never another pack's. */
    amend(this: void, block: string, hooks: BlockAmendSpec): void
        /** Load-time only: a world may already be holding blocks of a definition, so one that arrived later would change the rules under the players standing on it. */
    define(this: void, spec: BlockSpec): BlockDef
}

/** What a definition says a block *is*.  Every hook takes `base` as its **last** argument: call it and you extended what is under you, leave it out and you replaced it. `base` is a decision rather than a reentrant call — its effects land when your hook returns, and calling it twice happens once. */
interface BlockSpec {
        /** What a break leaves — and, because `on_break` fails closed, what it leaves when this pack is too slow to answer. */
    drops?: Drops | false
        /** A handle, a game block's name, a plain table of fields and hooks, or a list of those **innermost first**. */
    extends?: BlockRef | { [key: string]: any } | any[]
        /** Turns its front to whoever places it; `block.facing` reads and turns it. */
    facing?: boolean
        /** Seconds-scale, as vanilla's hardness is; below zero is unbreakable. */
    hardness?: number
        /** The block in a hand. */
    item?: ItemTable | false
        /** The name of the item a textured block comes with. */
    label?: Text
        /** What it gives off, 0 to 15. */
    light?: number
        /** A block state the client already draws, because a client has never heard of this pack. */
    looks?: string | string[]
        /** The jar's Material as five questions: solid, covers (grass under it dies), firm (snow and ice need it), liquid, burns. */
    material?: { solid?: boolean; covers?: boolean; firm?: boolean; liquid?: boolean; burns?: boolean }
        /** Its own shape on 1.21.4+, in place of `texture`: a model that stays inside the block, one for every state or one per state. */
    model?: Model | Model[]
        /** Without a namespace. */
    name: string
        /** It has just been stored, whatever stored it. */
    on_added?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** Something broke it. */
    on_break?: (this: void, block: BlockAt, player: Player, by: Breaker, base: (this: void, ...args: any[]) => any) => Drops | undefined
        /** A neighbour changed; `from` is its position and `announced` the block name the notifier announced itself as. */
    on_neighbour?: (this: void, block: BlockAt, from: Vec3, announced: string, base: (this: void, ...args: any[]) => any) => void
        /** A player put it down; `block.data` is empty then, ready to be filled. */
    on_place?: (this: void, block: BlockAt, player: Player, base: (this: void, ...args: any[]) => any) => void
        /** A redstone signal started (`powered` is true) or stopped reaching it. */
    on_power?: (this: void, block: BlockAt, powered: boolean, base: (this: void, ...args: any[]) => any) => void
        /** The random pass landed on it. */
    on_random_tick?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** It has just gone from the world. */
    on_removed?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** A body is standing on it; `body` is `{ id, kind }`. */
    on_step?: (this: void, block: BlockAt, body: Body, base: (this: void, ...args: any[]) => any) => void
        /** A scheduled tick this block asked for came due. */
    on_tick?: (this: void, block: BlockAt, base: (this: void, ...args: any[]) => any) => void
        /** It was lit, blasted or burnt; `cause` is "ignite", "explosion" or "fire". */
    on_trigger?: (this: void, block: BlockAt, cause: Trigger, base: (this: void, ...args: any[]) => any) => void
        /** The hooks. */
    on_use?: (this: void, block: BlockAt, player: Player | undefined, held: string, base: (this: void, ...args: any[]) => any) => Used | undefined
        /** What a step through it takes off the light; 15 is an opaque cube. */
    opacity?: number
        /** What it gives a redstone circuit, 0 or 15: one number for every face, a table keyed by face (the names `texture` takes), or a list of either with one entry per state. */
    power?: number | { [key: string]: number } | number | { [key: string]: number }[]
        /** What an explosion has to chew through. */
    resistance?: number
        /** Its own picture on 1.21.4+: one for every state, or one per state. */
    texture?: Faces | Faces[]
        /** Seconds between `block:schedule()` and `on_tick`; 0.5 unless you say. */
    tick_every?: number
}

/** What took a block out, and with what. */
interface Breaker {
        /** What took the block out: a player, fire, an explosion, flowing water, or the loss of what held it up ("support"). */
    cause: "player" | "fire" | "explosion" | "water" | "support"
        /** Whether a creative player broke it; creative takes the block and leaves nothing. */
    creative: boolean
        /** The item in hand, or nil for a bare hand and for the four causes that have none. */
    tool?: string
}

/** What a pack's tick and event callbacks are allowed per tick, together, and what it did with it. Milliseconds throughout. */
interface Budget {
        /** The engine's questions to this pack, and what it did with those. */
    asks: Asks
        /** Ordinary events lost to queue overflow. */
    dropped: number
        /** `budget_ms` in citadel.yml; 2 by default. */
    of: number
        /** The most any tick has spent. */
    peak: number
        /** Callbacks not run for want of budget, since the script started. */
    skipped: number
        /** The slowest single callback so far, by short hook name. */
    slowest?: { hook: string; ms: number }
        /** What the last tick spent. */
    used: number
}

/** What `world.build` hands the function it is given. Coordinates are whole blocks of the build's own and may be negative; later writes win. */
interface Builder {
        /** Sets one block of the build; later writes win. */
    block(pos: Vec3, block: string): void
        /** Inclusive corners, in any order, like `chunk:fill`. */
    box(from: Vec3, to: Vec3, block: string): void
        /** Every block the straight line between the ends passes through. */
    line(from: Vec3, to: Vec3, block: string): void
        /** What `fn` writes is a named part, found by `citadel render --part` and `citadel check` once pasted. */
    part(name: string, fn: (this: void) => void): void
}

/** A picture of one or more maps with no frame of its own, from `world.canvas`, for a frame display, a hand or a screen. */
interface Canvas {
        /** Removes the canvas; clients that saw it keep its last picture, and its id is never reused. */
    destroy(): void
        /** The map id of its top-left map, for a `filled_map`. */
    view(player: Player): View
}

/** [no documented members: opaque] */
interface ChaseCamera {
}

/** A 16 by 16 column of blocks, handed to `world.on_generate`, `world.on_populate` and a room's `generate` to fill. */
interface Chunk {
        /** Fills a box of blocks, clipped to the chunk. */
    fill(from: Vec3, to: Vec3, block: string): void
        /** Sets the biome of every column in a box, clipped to the chunk. */
    fill_biome(from: Vec3, to: Vec3, biome: string): void
        /** Chunk X coordinate (16 blocks each). */
    get(pos: Vec3): string
        /** Returns the biome of the column at `pos`, by name; `nil` outside the chunk. */
    get_biome(pos: Vec3): string | undefined
        /** Clipped to this chunk; air is skipped unless `air` is true. */
    paste(schem: Schematic, origin: Vec3, opts?: { air?: boolean; part?: string }): void
        /** Sets one block; positions outside the chunk are ignored. */
    set(pos: Vec3, block: string): void
        /** Sets the biome of one column: a vanilla name ("desert") or the name `game.biomes.define` returned. */
    set_biome(pos: Vec3, biome: string): void
}

/** A command a pack added, from `commands.add`; change its suggestions or `cancel` it. */
interface Command {
        /** Takes the command away. */
    cancel(): void
        /** What `arg` offers from now on: a list, a function, or nil or false for nothing. */
    suggest(arg: string, words?: Suggestion[] | Suggester | false): void
}

/** The options of `commands.add`: a permission node, aliases, the /help line and suggestions per argument. */
interface CommandOpts {
        /** More names for the same command: { "hub", "lobby" }. */
    aliases?: string[]
        /** The line /help shows after the usage. */
    help?: string
        /** A permission node; without it the command is not shown and not run. */
    permission?: string
        /** Per argument name: the words to offer, or a function that returns them. */
    suggest?: { [key: string]: Suggestion[] | Suggester }
}

/** An event subscription or repeating timer; task functions return threads. */
interface Connection {
        /** Stops the subscription or repeating timer, including from its own callback. */
    cancel(): void
}

/** A chest's stacks: `world.container(pos)`. A chest a player has open is theirs until it closes — `take` takes nothing, `put` puts nothing. */
interface Container {
        /** The chest's block position. */
    at: Vec3
        /** The filled slots, in order. */
    items(): InventorySlot & { slot: number }[]
        /** How many did not fit; 0 when all of it went in. */
    put(item: ItemSpec): number
        /** How many slots the chest has, e.g. */
    size: number
        /** Up to `count` (1 unless you say) of what matches; how many it took. */
    take(item: ItemMatch, count?: number): number
}

/** A hit on a player, before it lands: what `players.on_damage` hands a pack. */
interface DamageHit {
        /** Half hearts, before armour. */
    amount: number
        /** The player who hit, or who shot the arrow. */
    by?: Player
        /** "fall", "drown", "suffocate", "void", "lava", "fire", "cactus", "starve", "attack", "shot", "blast" or "magic". */
    cause: string
        /** The kind's name ("Skeleton") when a mob did it. */
    kind?: string
}

/** An open dialog, from `player.ui.dialog`. */
interface Dialog {
        /** Closes it. */
    destroy(): void
        /** Whether the player still has it open. */
    refresh(): void
        /** A new view in place: a window, or a function that makes one. */
    update(view: DialogNode | ((this: void) => DialogNode)): void
}

/** An item, text, block or frame shown in the world, from `world.display`; its place, rotation, scale and look are live. */
interface Display {
        /** Makes one tweened change of place, scale, rotation or text over `duration` seconds (0.5 by default), played by the client. */
    animate(opts: { at?: Vec3; scale?: Vec3 | number; rotation?: Orientation; text?: Text; color?: Ink; background?: Ink | false; line_width?: number; shadow?: boolean; duration?: number }): void
        /** Text kind: the colour behind the words; nil or false for none. */
    background?: Color | false
        /** Whether it is still present. */
    billboard: Billboard
        /** block kind. */
    block?: string
        /** Item kind: the canvas shown as a filled map; written as a canvas, read back as its map id. */
    canvas?: number
        /** The colour of the words that did not pick one. */
    color?: Color
        /** Item kind: how the item is posed, as in a frame, a hand or on the ground. */
    context?: Context
    destroy(): void
        /** Seconds later changes take to play out on the client (1.19.4 and later); 0 by default. */
    duration: number
        /** Advanced movement smoothing in seconds (1.20.2+); default 0.1, 0 follows duration. */
    glide: number
        /** Its outline colour; nil or false for none. */
    glow?: Color | false
        /** The raw entity id. */
    id: number
        /** item kind. */
    item?: string
        /** Advanced: true enables linear prediction. */
    lead?: boolean
        /** Text kind: the width its lines wrap at; 200 by default. */
    line_width?: number
        /** Removes the display. */
    move(at: Vec3, rotation?: Orientation): void
        /** Text kind: whether the words have a shadow; false by default. */
    shadow?: boolean
        /** text kind Reads back the words; takes any text. */
    text?: string
}

/** Shared durable stores. Calls yield; pcall catches structured errors such as {err = "conflict", version = 3}. One store per experience. */
interface DurableStore {
        /** Deletes a player's blob if its version is still `if_version`. */
    blob_delete(owner: string, key: string, if_version: number, lease?: number): void
        /** Returns one player's binary blob, or nil, and its version; `owner` is the player's uuid. */
    blob_get(owner: string, key: string): LuaMultiReturn<[string | undefined, number]>
        /** Writes a player's binary blob if its version is still `if_version`, and returns the new version. */
    blob_put(owner: string, key: string, bytes: string, if_version: number, lease?: number): number
        /** Removes a fact if its version is still `if_version`. */
    delete(key: string, if_version: number, lease?: number): void
        /** Returns a fact's value and its version; version 0 means absent. */
    get(key: string): LuaMultiReturn<[any, number]>
        /** Adds `by` to a number atomically, starting at zero, and returns the result. */
    increment(key: string, by: number): number
        /** Returns fact keys with this prefix and the cursor for the next page, or nil at the end. */
    list(prefix?: string, cursor?: string, limit?: number): LuaMultiReturn<[string[], string | undefined]>
        /** Writes a fact if its version is still `if_version`, and returns the new version. */
    set(key: string, value: any, if_version: number, lease?: number): number
}

/** `game.entities`: the three verbs over one shape. */
interface Entities {
        /** The game's own content only — never another pack's. */
    amend(this: void, name: string, hooks: EntityAmendSpec, options?: EntityAmendOptions): void
        /** Load time only. */
    define(this: void, spec: EntitySpec): EntityDef
        /** Every kind by name: the pack's own and the game's, mob or not. */
    names(this: void, query?: { mob?: boolean }): string[]
}

interface EntityAmendSpec {
        /** Asked when it takes damage; return "ignore" to cancel it. */
    on_damage?: (this: void, e: EntityHandle, amount: number) => "take" | "ignore" | undefined
        /** Called for an entity that already existed: a saved chunk loaded it, or a reload rebound it. */
    on_load?: (this: void, e: EntityHandle) => void
        /** Called when it leaves the world; `why` is "removed", "settled", "killed" or "unloaded". */
    on_remove?: (this: void, e: EntityHandle, why: string) => void
        /** Called when a new entity of this kind spawns; told, never waited on. */
    on_spawn?: (this: void, e: EntityHandle) => void
        /** Wrapped behavior runs first unless options.replace = true. */
    on_steer?: (this: void, e: EntityHandle, base: (this: void) => void) => void
        /** Wrapped behavior runs first unless options.replace = true. */
    on_tick?: (this: void, e: EntityHandle, base: (this: void) => void) => void
}

/** [no documented members: opaque] */
interface EntityCamera {
}

/** A body the world moves: a pack's own entity, a mob, a stack on the ground.  Every read is a fresh look at the world, so a handle to something that has died reads `nil`. Inside a hook the same handle reads the entity as it was at the top of the tick, and its writes land at that hook's own slot. */
interface EntityHandle {
        /** Ticks lived. */
    age?: number
        /** Whether it is still in the world. */
    alive: boolean
        /** A pack-defined entity's attached record. */
    data: DataView
    destroy(): boolean
        /** Whether it is in water now. */
    driver?: Player
        /** Intent, a living body with can_fly only: true flies (no gravity; forward moves it along its look, pitch included), false falls and walks. */
    flying: boolean
        /** The intent fields: what a body *wants* to do, which is what steering is. */
    forward: number
        /** Its health now. */
    health?: number
        /** Whether its kind is hostile. */
    hostile?: boolean
        /** Its entity id, the one players.on_click reports in `hit.entity_id`. */
    id: number
        /** Intent: whether it wants to jump. */
    jumping: boolean
        /** The most health its kind gives it. */
    max_health?: number
        /** Gone on the next tick. */
    move(at: Vec3, rotation?: BodyRotation): void
        /** The kind's name: "cow", "rave:rocket". */
    name?: string
        /** What else is around it, by horizontal distance. */
    nearby(radius: number): EntityHandle[]
        /** Whether it stands on something. */
    on_ground?: boolean
        /** The block it used to be, for anything that arrived through a transition; nil for anything that was never a block. */
    origin?: string
        /** Every occupant by seat number, including NPCs; nil means empty. */
    paint: { [key: string]: Ink }
        /** Which order of operations moves it: "vehicle", "living", "falling", "item" or "none". */
    physics?: Physics
        /** Model size: reads vec3; write a positive number or equal-axis vec3. */
    play(animation: string, opts?: { speed?: number }): void
        /** A shove, in blocks a tick, added to what it is already doing. */
    push(v: Vec3): boolean
        /** It stops being an entity and is a block again where it stands. */
    settle(): boolean
        /** Stops a model entity's animation; the parts stay where they are. */
    stop(animation: string): void
        /** Intent: 1 left, -1 right. */
    strafe: number
        /** Where it is, live; writing it is a teleport. */
    velocity?: Vec3
}

/** One kind the game version has, in its own numbers, from `game.entities.<kind>`: name, size, max_health, speed and drop. A kind that is not a mob (an arrow, a boat, primed TNT; `mob == false`) has `name`, `mob`, `width`, `height` and `physics` only: every other fact is nil for it, and a write to `spawn`, `attacks` or `interact` and a call of `amend` are errors. */
interface EntityKind {
        /** The same as `game.entities.amend(name, hooks)`. */
    amend(hooks: EntityAmendSpec, options?: EntityAmendOptions): void
        /** Whether its hits hurt players. */
    attacks?: boolean
        /** The name of the behaviour the engine runs for this kind, such as "sheep" or "living". */
    behaviour: string
        /** The item its death leaves behind, such as "leather"; nil for none. */
    drop?: string
        /** Its height in blocks, in this version's numbers. */
    height: number
        /** Whether it is hostile. */
    hostile: boolean
        /** Whether a player's right click on it has the game's effect (milk, a saddle). */
    interact?: boolean
        /** The most health one of this kind has, in this version's numbers. */
    max_health: number
        /** Whether the kind is a mob: true for a cow, false for an arrow. */
    mob: boolean
        /** Its modern registry name: "cow". */
    name: string
        /** For a kind that is not a mob, which order of operations moves it: "item", "falling", "vehicle" or "none". */
    physics?: string
        /** Read-only copy; nil for a specialized behavior without a shared profile. */
    profile?: { [key: string]: string | number | boolean }
        /** This version's own registry spelling: "Cow". */
    registry_name: string
        /** The one writable field. */
    spawn?: boolean
        /** Blocks a tick at a full walk. */
    speed: number
        /** Its width in blocks, in this version's numbers. */
    width: number
}

/** A kind of entity a pack makes up. `base` is the last argument of every hook: call it and you extended, don't and you replaced. */
interface EntitySpec {
        /** physics = "vehicle" only: seconds from standing to top speed; 1 by default. */
    accel?: number
        /** physics = "living" only: it may fly when its pack sets e.flying = true, and it takes no fall damage. */
    can_fly?: boolean
        /** physics = "living" only: what it leaves when it dies. */
    drops?: ({ [key: string]: any })[] | false
        /** What a client older than 1.21.4 sees in place of the model, such as "minecart". */
    fallback?: string
        /** A shape the client draws, or a model from models.new. */
    looks: Looks | Model
        /** physics = "living" only: the most health it has, and what it starts with. */
    max_health?: number
        /** Your own word for the kind, lower case, digits and underscores; the pack's namespace is added for you ("rocket" is "rave:rocket"). */
    name: string
        /** Asked when a player hits it: answer "take" or "ignore". */
    on_damage?: (this: void, e: EntityHandle, amount: number, by: Player) => "take" | "ignore" | undefined
        /** Told when one that already existed comes back: a saved chunk loaded it or a reload rebound it. */
    on_load?: (this: void, e: EntityHandle) => void
        /** Told when it goes; `why` is "removed", "settled", "killed" or "unloaded". */
    on_remove?: (this: void, e: EntityHandle, why: string) => void
        /** Told when one of this kind is spawned; nothing waits on it and its answer is not read. */
    on_spawn?: (this: void, e: EntityHandle) => void
        /** Runs before the physics each tick to decide where it goes; call `base(e)` to extend, leave it out to replace. */
    on_steer?: (this: void, e: EntityHandle, base: (this: void) => void) => void
        /** define only. */
    on_think?: (this: void, b: Think) => void
        /** Runs after the physics each tick to react to where it ended up; call `base(e)` to extend. */
    on_tick?: (this: void, e: EntityHandle, base: (this: void) => void) => void
        /** "save" brings it back with its chunk, `data` and all; "despawn", the default, is gone when the chunk goes. */
    persist?: Persist
        /** Which order of operations moves it: "living", "falling", "item", "none", or "vehicle" to drive by seat 1's keys. */
    physics?: Physics
        /** A model's size; 1 by default. */
    scale?: number
        /** A model's: where riders sit (model units, seat 1 drives), its size, and what a client older than 1.21.4 sees. */
    seats?: Vec3[]
        /** One number, or { width, height }. */
    size?: number | number[]
        /** physics = "living" only: sound names for its hurt, its death and its idle sound, vanilla or "<pack>.<file>". */
    sounds?: { hurt?: string; death?: string; ambient?: string } | false
        /** How fast it goes, in blocks a second. */
    speed?: number
        /** physics = "vehicle" only: blocks it climbs without a jump; 1 by default. */
    step?: number
        /** define only. */
    think_every?: number
        /** physics = "vehicle" only: degrees a second it turns at speed; 90 by default. */
    turn?: number
}

/** A number at every block, as a recipe the engine works out. Sums (`+ - * / ^` and unary minus) and the methods make new fields; a plain number is a field too. A field above 0.5 is "true" where a rule asks a question. */
interface Field {
    abs(): Field
        /** This field read `dx, dy, dz` blocks away: `fields.water:at(1, 0, 0)` is the water east of here. */
    at(dx: number, dy: number, dz: number): Field
    clamp(low: number, high: number): Field
        /** Straight lines through `{ { input, output }, .. */
    curve(points: (number[])[]): Field
    floor(): Field
        /** 1 where this is the larger, else 0. */
    gt(other: Field | number): Field
        /** 1 where this is the smaller, else 0. */
    lt(other: Field | number): Field
    max(other: Field | number): Field
    min(other: Field | number): Field
        /** 0 at `from`, 1 at `to`, smooth between. */
    smooth(from: number, to: number): Field
    sqrt(): Field
}

/** Camera modes expose only the fields they use. Values shared across players update all their views. A removed target reads nil and ends the active view. [no documented members: opaque] */
interface FixedCamera {
}

/** [no documented members: opaque] */
interface FreeCamera {
}

/** A declared world, for the script to ask what the engine answers. */
interface Generated {
        /** Returns the biome name a column gets. */
    biome_at(pos: Vec3): string | undefined
        /** Returns a field's value at a position; `nil` for a field made after `world.generate`, or for rules with no `height`. */
    sample(field: Field | number, pos: Vec3): number | undefined
}

/** What `world.generate` takes. Without `height` and `density`, the rules add to the land the game's own terrain made. */
interface GeneratorRules {
        /** `{ "desert", when = field }`: the first that holds names the column's biome; one with no `when` is for the rest. */
    biomes?: ({ [key: number]: string; when?: Field | number })[]
        /** The game version's own carvers, with the world seed, after the land and before the cave rules: "caves" (every version), "ravines" (b1.8 and later). */
    carvers?: "caves" | "ravines"[]
        /** Solid where this is above 0, for caves, overhangs and land in the air. */
    density?: Field
        /** The block at y 0; "bedrock" for a land of its own. */
    floor?: string
    fluid?: string
        /** What fills the caves: needs `density` or `carvers`. */
    fluids?: FluidRule[]
        /** The y of the surface. */
    height?: Field | number
    plants?: PlantRule[]
        /** The body of the land, under the ground rules. */
    rock?: GroundRule[]
        /** Water fills the open air up to this y. */
    sea?: number
        /** The game version's own structures, with spawners and loot: "mineshaft", "dungeon" (1.7 to 1.12). */
    structures?: "mineshaft" | "dungeon"[]
    surface?: GroundRule[]
    things?: ThingGrid[]
}

/** What `players.on_click` hands its callback: the button, the slot, and the player, entity, block and face the click met. */
interface Hit {
        /** The block, when the click hit one. */
    block?: Vec3
        /** "left" is an attack or swing, "right" is an interact or use. */
    button: "left" | "right"
        /** The thing clicked, as the handle the script holds for it. */
    entity?: Display | Hitbox | Npc | Puppet
        /** Its raw entity id, which is all there is for something the engine made itself, such as one of a screen's own frames. */
    entity_id?: number
        /** The face of the block that was clicked. */
    face?: Face
        /** Another player, when that is what was clicked. */
    player?: Player
        /** The hotbar slot in hand, 1..9. */
    slot: number
}

/** An invisible box a player can click, and a wall when solid, from `world.hitbox` (1.19.4 and later). */
interface Hitbox {
        /** Its bottom centre; write it to move the hitbox, and its wall when solid. */
    at: Vec3
        /** Removes the hitbox, and its wall when solid. */
    destroy(): void
        /** Its entity id, what `players.on_click` reports in `hit.entity_id`. */
    id: number
}

/** What `http.get` returns. A failed request is not an error: read `ok`. */
interface HttpResponse {
        /** The answer as bytes. */
    body: string
        /** Why no answer came, or nil. */
    error?: string
        /** The answer's headers, names in lower case. */
    headers: { [key: string]: string }
        /** A PNG body: `pixels` is 4 bytes (RGBA) a pixel, row by row from the top. */
    image(): { width: number; height: number; pixels: buffer }
        /** The body as a table; an error when it is not JSON. */
    json(): any
        /** True for a 2xx status. */
    ok: boolean
        /** The HTTP status; 0 when no answer came. */
    status: number
}

/** A layout on one player's screen, from `player.ui.show`. `hud.<id>` is the item with that id. */
interface Hud {
        /** Where the pointer is, in the layout's pixels from its top left. */
    cursor?: { x: number; y: number }
        /** Takes it off the player's screen. */
    destroy(): void
        /** With `cursor = true`: the id under the pointer, and what fires when it changes and on a click. */
    hover?: string
    on_click(this: void, arg0: (this: void, id: string, button: "left" | "right") => void): unknown
    on_hover(this: void, arg0: (this: void, id: string) => void): unknown
        /** A value per id: a number is a fill, a string a label's words, true or false whether it shows. */
    set(values: { [key: string]: number | string | boolean }): void
}

/** One item of a shown layout, `hud.hp`: its live values. They tween. */
interface HudPart {
        /** A box's colour, a picture's tint, a label's ink; reads back as "#rrggbb". */
    color?: Ink
        /** How much of a box or picture shows, from its left edge: 0 to 1. */
    fill: number
        /** A label's words. */
    text: string
        /** Whether it shows; nil shows it again. */
    visible?: boolean
}

/** The extras an item table may carry: count, name, lore, colours, glint, a canvas map, a pack item id, wear, a 1.21.4+ model and a head's skin. */
interface ItemMeta {
        /** A filled map of that canvas: what the item *is*, so `item` may be left out. */
    canvas?: Canvas
        /** A potion's liquid colour; 1.11 and later. */
    color?: Color
        /** How many in the stack; 1 by default. */
    count?: number
        /** The wear a tool has taken; 0 is new. */
    damage?: number
        /** Leather armour's colour. */
    dye?: Color
        /** The enchanted shine, with no enchantment. */
    glint?: boolean
        /** A pack's own item: a brick with `id = "copper_ingot"` is a copper ingot, kept under the pack's name and known by it everywhere it goes. */
    id?: string
        /** One line or a list of lines, grey unless they say otherwise. */
    lore?: Text[] | Text
        /** The item model a 1.21.4+ client draws: `assets/<pack>/items/<model>.json`. */
    model?: string
        /** Never italic unless it says so. */
    name?: Text
        /** The face a "player_head" item shows: a player's name, or the raw `textures` property. */
    skin?: string | { value: string; signature?: string }
}

/** `game.items`: items of the pack's own. */
interface Items {
        /** Load-time only. */
    define(this: void, spec: { name: string; texture?: TextureRef; label?: Text; lore?: Text[] | Text; looks?: string; stack?: number; glint?: boolean }): ItemTable
}

/** A block's material as five yes-or-no questions, from `block.material`: solid, covers, firm, liquid and burns. */
interface Material {
        /** Whether the jar's Material burns. */
    burns: boolean
        /** Grass under it dies. */
    covers: boolean
        /** Snow and ice need it beneath them. */
    firm: boolean
        /** Whether the jar's Material is a liquid. */
    liquid: boolean
        /** Whether the jar's Material counts as solid. */
    solid: boolean
}

/** An open menu, from `player.ui.menu`. */
interface Menu {
        /** Takes it down and forgets its callbacks. */
    destroy(): void
        /** New pictures in place, the menu left open: a bar that fills, a count that changes. */
    update(items: ItemSpec[]): boolean
}

/** A model the pack made, for `world.display{ kind = "model" }`. */
interface Model {
        /** The name the model was given in `models.new`. */
    name: string
}

/** What `models.new` hands its build function: makes the model's materials, textures, parts and animations. */
interface ModelBuild {
        /** `{ length = seconds, loop = false, <part name> = { rotation = { [t] = is both named fields and part names, so this one is open. */
    animation(name: string, opts: { [key: string]: any }): void
        /** Makes a named colour a display may repaint; `grain` (0 to 1) darkens pixels into four tones, `alpha` below 1 is glass. */
    material(name: string, color: Ink, opts?: { grain?: number; alpha?: number }): ModelMaterial
        /** Makes a named child part of the root that turns around its `pivot`, the model's origin unless given. */
    part(name: string, opts?: { pivot?: Vec3 }): ModelPart
        /** Makes a pixel picture for one face; with `tint`, drawn in greys and coloured by that material. */
    texture(width: number, height: number, opts?: { tint?: ModelMaterial; scroll?: "up" | "down" | "left" | "right"; speed?: number }): ModelTexture
}

/** A model visual in a room. Shares at, rotation, scale, alive and move with other visuals; adds named animations and model materials. */
interface ModelDisplay {
        /** Removes the model from the room. */
    destroy(): void
        /** What `player:ride(model)` is handed; the seat is picked from `seats`. */
    id: number
        /** Place and turn it in one step, every part and seat together. */
    move(at: Vec3, rotation?: Orientation): void
        /** Whether it is still present. */
    paint: { [key: string]: Ink }
        /** Starts an animation; replaying the current one changes speed without restarting. */
    play(animation: string, opts?: { speed?: number }): void
        /** Where it is; the parts stay as they are. */
    stop(animation: string): void
}

/** A flat colour in a model. A display repaints it by this name. */
interface ModelMaterial {
        /** The name it was made with, which a display repaints it by. */
    name: string
}

/** A named group of boxes that turns around its pivot. Units are 16 to the block, the origin is the model's bottom centre, and a box reaches -24..24. */
interface ModelPart {
        /** Corners in any order; a box turns on one axis, in steps of 22.5 up to 45, and `pivot` is the box's own centre unless you give one. */
    box(from: Vec3, to: Vec3, skin: ModelSkin, opts?: { rotation?: Vec3; pivot?: Vec3; faces?: { [K in Face]: ModelSkin } }): void
        /** A box a player can hit on a living body that wears the model (clients from 1.19.4). */
    hitbox(from: Vec3, to: Vec3): void
        /** A mirrored copy of every box and hitbox this part has, and a mirrored twin named `<name>_mirrored` of every child. */
    mirror(axis: "x"): void
        /** Makes a child part of this one; it turns around `pivot`, the model's origin unless you give one. */
    part(name: string, opts?: { pivot?: Vec3 }): ModelPart
}

/** Pixel art for one face of a box: plain RGBA, and never repainted. */
interface ModelTexture {
        /** A game.texture over this one, its top left at x, y; see-through pixels skipped, what falls outside cut. */
    draw(picture: Texture, x?: number, y?: number): void
        /** Paints every pixel one colour. */
    fill(color: Ink): void
        /** Paints the pixel at x, y; `colors.transparent` makes it see-through. */
    pixel(x: number, y: number, color: Ink): void
        /** Paints a rectangle `w` by `h` pixels from x, y. */
    rect(x: number, y: number, w: number, h: number, color: Ink): void
}

/** An instance of a member: a server the network started for itself. */
interface NetworkInstance {
        /** The instance's name. */
    id: string
    label: string
    member: string
        /** The instance's own value. */
    meta: any
        /** The number of players it takes now, as it said with `network.status`. */
    open?: number
        /** The number of players on it. */
    players?: number
        /** "starting", then "online", then "stopping". */
    state: string
        /** The instance's own word. */
    status?: string
}

/** What `network.start` and `network.find` answer. */
interface NetworkStarted {
    id: string
        /** "starting" or "online". */
    state: string
}

/** Smooth random numbers from `noise.new`: the same seed gives the same numbers every time. */
interface Noise {
        /** Returns about -1..1 at a point: `get(x, z)` for a height map, `get(x, y, z)` for caves and overhangs. */
    get(x: number, y_or_z: number, z?: number): number
        /** Returns `width * depth` heights in one call, row by row: the number for `(x + dx, z + dz)` is at `[dz * width + dx + 1]`. */
    grid(x: number, z: number, width: number, depth: number): number[]
}

/** A player-shaped entity every client from 1.8 sees, from `world.npc`; it can walk, talk, hold items, wear armour and ride. */
interface Npc {
    destroy(): void
        /** Gets off where it sits; set `at` after it to put it somewhere else. */
    dismount(): void
        /** Puts an item in the main hand; nil or false empties it. */
    hold(item?: ItemSpec | false): void
        /** The entity id, what `players.on_click` reports in `hit.entity_id`. */
    id: number
        /** Where it stands; live, so setting it moves the NPC. */
    look_at(pos: Vec3): void
        /** Removes the NPC. */
    move(at: Vec3, rotation?: BodyRotation): void
        /** Whether it is still present. */
    name: string
        /** How the body is held; live. */
    pose: NpcPose
        /** Sits in a seat as `player:ride` does, and never drives; `false` when somebody sits there. */
    ride(thing: MountTarget, opts?: { seat?: number }): boolean
        /** Whether it sits in a seat; live. */
    riding: boolean
        /** Sends a chat line "<name> ..." to the room, or just the words for an NPC with no name. */
    say(text: Text, color?: Ink): void
        /** Plays the arm swing animation. */
    swing(): void
        /** Walks the points by itself, facing where it goes; nil stops it. */
    walk(opts?: { path: Vec3[]; speed?: number; loop?: boolean }): void
        /** True while it walks a path, until the last point; never false with `loop`. */
    walking: boolean
        /** Puts armour on it, head first; each piece is an item. */
    wear(pieces: Worn): void
}

/** [no documented members: opaque] */
interface OrbitCamera {
}

/** A canvas on one player's screen, from `player.ui.overlay`: 128 by 128, drawn like a canvas. Row 0 is the engine's and never shows; draw in rows 1 to 127. Colour `colors.transparent` shows the game through it. */
interface Overlay {
        /** Takes it off the player's screen. */
    destroy(): void
        /** True until `destroy` or the player leaves. */
    open: boolean
}

/** A named part of a stored world (`world: <folder>`) and the generator that writes it. Declared, not run: `citadel generate <pack> --part <name>`, or `/part generate <name>` in build mode, runs it; a changed file runs it again while nobody has edited the part. See "parts" in docs/luau-api.md. */
interface PartDefinition {
        /** Where the build's block (0, 0, 0) lands. */
    at: Vec3
        /** Exactly a world.build function. */
    build(this: void, b: Builder): void
        /** 1 (whole blocks, the default) or 2 (half blocks), as world.build. */
    detail?: number
        /** Unique; a path, "downtown/tower-3", nests. */
    name: string
}

/** The calls a screen, a canvas and a view all share. */
interface Picture {
        /** Fills a circle of radius `r` pixels around (x, y). */
    circle(x: number, y: number, r: number, color: Ink): void
        /** Its width in pixels: 128 for each map across. */
    clear(color?: Ink): void
        /** Draws another screen, canvas or view with its top-left at (x, y), skipping its transparent pixels. */
    draw(source: Screen | Canvas | View, x?: number, y?: number): void
        /** Fills a w by h box of pixels with one colour, its top-left at (x, y). */
    fill(x: number, y: number, w: number, h: number, color: Ink): void
        /** Fills a box that fades from `from` to `to`, top to bottom; `"across"` runs it left to right. */
    gradient(x: number, y: number, w: number, h: number, from: Ink, to: Ink, across?: string): void
        /** Draws a smoothed line with round ends, `width` pixels wide (1 by default); positions may be fractions. */
    line(x0: number, y0: number, x1: number, y1: number, color: Ink, width?: number): void
        /** The width in pixels that `text` would draw, without drawing it; for centring. */
    measure(text: string, size?: number): number
        /** One map of the picture, `{ id = . */
    part(col: number, row: number): { id: number }
        /** Writes raw RGB bytes (a buffer or a string), three a pixel, row by row, into a w by h box. */
    pixels(x: number, y: number, w: number, h: number, data: buffer | string): void
        /** Plays a raw RGB video file from the pack at `fps` 0.5 to 20, the engine drawing each frame; returns the Video. */
    play(opts: { file: string; fps?: number; loop?: boolean }): Video
        /** Fills a smoothed shape with any number of corners; a point is `{x, y}` or `{ x = .., y = . */
    polygon(points: (number[] | { x: number; y: number })[], color: Ink): void
        /** Fills a box like `fill`, with smoothed rounded corners of `radius` pixels when given. */
    rect(x: number, y: number, w: number, h: number, color: Ink, radius?: number): void
        /** Draws a circle's outline, `width` pixels wide (1 by default), smoothed. */
    ring(x: number, y: number, r: number, color: Ink, width?: number): void
        /** Paints one pixel; (0, 0) is the top-left. */
    set(x: number, y: number, color: Ink): void
        /** Draws pixel art: each string a row, each character a dot `scale` pixels square (1 by default); a character with no ink is skipped. */
    sprite(x: number, y: number, rows: string[], inks: { [key: string]: Ink }, scale?: number): void
        /** Draws text in DejaVu Sans Bold, `size` pixels tall (16 by default), smoothed; returns its width in pixels. */
    text(x: number, y: number, text: string, color: Ink, size?: number): number
}

/** A plant on a column. Each column takes at most one: a rule that holds is tried with its `chance` (1), in the order of the list. */
interface PlantRule {
        /** On the water over a column, not on its ground. */
    afloat?: boolean
    biome?: string
    block?: BlockPick
        /** The blocks from the foot up, in place of `block`: a two-block flower. */
    blocks?: BlockPick[]
    chance?: Field | number
        /** Blocks of water to keep clear over a plant that grows in it. */
    clear?: number
        /** How many blocks a plant that grows is tall: `block` repeats. */
    height?: Field | number
        /** Where it goes: "top" (the default), or in the caves `density` or `carvers` dig: "floor", "ceiling" (it hangs down: `tip` is lowest) or "wall" (one block; `{wall}` in its name is the side the rock is on, `{facing}` the side away). */
    place?: "top" | "floor" | "ceiling" | "wall"
        /** Blocks to stand lower: 1 is in the ground, or in the top of the water. */
    sink?: number
        /** With `height`, the block on top of a plant that grows. */
    tip?: BlockPick
    when?: Field | number
        /** `{ low, high }`: the y it may start at. */
    y?: number[]
}

/** A player in the room: what `players.on_join` and every player event hand you. */
interface Player {
    /** `player.ui` — this player's own ui table. Source: official HUD
     *  doc (player.ui.overlay). */
    ui: PlayerUi;
        /** Puts the player in a group until they leave; errors on a group citadel.yml does not define. */
    add_group(group: string): void
        /** What they look out of: a camera from camera.fixed/free/orbit/chase, or nil or false for their own eyes. */
    camera?: Camera | false
        /** May fly in a mode that cannot. */
    can_fly: boolean
        /** True unless `other` is not visible or is hidden from this player. */
    can_see(other: Player): boolean
        /** Takes a potion effect off the player, by its modern name. */
    clear_effect(name: string): void
        /** Asks Minefort to move the player to another server by name: an instance's `id`, the network's name (its default member) or "hub". */
    connect(server: string): void
        /** Returns how many of an item the player carries, across every slot. */
    count(item: ItemMatch): number
        /** A hit in half-hearts: the flash, the sound, the resistance window. */
    damage(amount: number): boolean
        /** Gets the player off what they ride; sneaking does the same, as off a horse. */
    dismount(): void
        /** A potion effect by its modern name; `duration` in seconds, math.huge for ever. */
    effect(name: string, opts?: { level?: number; duration?: number; particles?: boolean }): void
        /** The hotbar slot in hand, 1..9; live. */
    gamemode: number
        /** One item: "stone", or { item = "arrow", count = 16 }. */
    give(item: ItemSpec): void
        /** Returns the player's groups; `default` is not listed. */
    groups(): string[]
        /** True if the player's groups give them this permission node; operators have every node. */
    has(node: string): boolean
        /** Returns the stack in hand ({ item, count }, plus `id` for a pack item and `damage` for a worn tool), or nil. */
    held(): InventorySlot | undefined
        /** This player stops seeing `other`, or sees them again. */
    hide(other: Player): void
        /** Replaces the nine hotbar slots; a missing index is empty. */
    hotbar(slots: { [key: number]: ItemTable }): void
        /** Returns one { item, count } row per filled slot. */
    inventory(): InventorySlot[]
        /** Disconnects the player, with that text on their screen. */
    kick(reason?: Text): void
        /** 0..20, or nil where the game version has no food bar. */
    kill(): boolean
        /** The experience bar: the number over it, and how full it is (0..1). */
    level: number
        /** Returns the unit vector the player faces. */
    look(): Vec3
        /** Turns the player's head to a point, where they stand. */
    look_at(pos: Vec3): void
        /** Their health now, 0 to `max_health`; nil where the game version has no damage rules. */
    max_health?: number
        /** What shows on this player's screen: the calls `ui` has, for them alone, plus their own menu and overlay. */
    message(text: Text, color?: Ink): void
        /** Moves the player to another room; the client swaps worlds in place. */
    move_to(room: Room): void
        /** A shove in blocks per tick, on top of what they are doing. */
    push(velocity: Vec3): void
        /** How far a block can be clicked or dug, 0 to 64 blocks (4.5 by default); 1.20.5 and later. */
    reach: number
        /** Takes the player out of a group. */
    remove_group(group: string): void
        /** The player's name. */
    ride(thing: MountTarget, opts?: { seat?: number; locked?: boolean }): boolean
        /** 1/16 to 16; 1.20.5 and later, older clients stay as they are. */
    scale: number
        /** The stack in hand, replaced; nil or false empties the hand. */
    set_held(item?: ItemSpec | false): void
        /** Selects hotbar slot 1..9. */
    set_slot(n: number): void
        /** This player sees `other` again after a `hide`. */
    show(other: Player): void
        /** Plays a sound by name to this player only, with an optional position, volume, pitch and category. */
    sound(name: string, opts?: { at?: Vec3; volume?: number; pitch?: number; category?: string }): void
        /** The player's own respawn point (the block of the position), or nil for the room's. */
    spawn_point?: Vec3
        /** The body: what a pack sets on a player. */
    speed: number
        /** Where their view is from: the camera they look out of, or their eyes. */
    stop_sound(name?: string): void
        /** True if this player's client can show the feature. */
    supports(feature: Feature): boolean
        /** Up to `count` (1 unless you say) of what matches, the hand first; answers how many it took. */
    take(item: ItemMatch, count?: number): number
        /** Yaw and pitch left out keep the way they face. */
    teleport(pos: Vec3, rotation?: BodyRotation): void
        /** This player's sky alone, held at a time of day; nil or false gives them the room's again, as does moving rooms. */
    time?: number | TimeName | false
        /** Sends the player to another world of the group, at `pos` or its spawn. */
    travel(dimension: string, pos?: Vec3): void
        /** false: no other player is sent this body. */
    visible?: boolean
        /** The four armour slots; a piece left out is bare. */
    wear(pieces: Worn): void
        /** How full the experience bar is, 0..1. */
    xp: number
}

/** `player.ui`: the calls `ui` has, for one player alone, plus what only one player's screen holds. */
interface PlayerUi {
        /** A screen of boxes, words and pictures (see "Dialogs"): a `ui.kit.window{}`, or a function that returns one and is drawn again after every click. */
    dialog(this: void, view: DialogNode | ((this: void) => DialogNode)): Dialog | undefined
        /** A titled grid of up to 54 items over the player's view; each pick is answered by `on_pick(player, n)`. */
    menu(this: void, opts: { title?: Text; items: ItemSpec[]; on_pick: (this: void, player: Player, n: number) => void; on_close?: (this: void, player: Player) => void }): Menu
        /** Puts a canvas in a corner of this player's screen, `size` screen pixels square at GUI scale 1 (96 by default, 16 to 511), `margin` from the edges (4 by default); nil where `player:supports("overlay")` is false. */
    overlay(this: void, opts?: { corner?: "top_left" | "top_right" | "bottom_left" | "bottom_right"; size?: number; margin?: number }): Overlay | undefined
        /** Puts a layout on this player's screen. */
    show(this: void, layout: Layout): Hud
}

/** A mob's body with no mind of its own that the script moves, from `world.puppet`; its name tag always shows. */
interface Puppet {
        /** Removes the puppet. */
    destroy(): void
        /** The raw entity id. */
    id: number
    move(at: Vec3, rotation?: BodyRotation): void
        /** The text of its name tag, which is always shown. */
    name?: string
}

/** `game.recipes`: what a crafting grid and a furnace make of a pack's items. Load-time only, like a block definition. The game's own recipes are asked first, so a pack adds and never takes away. */
interface Recipes {
        /** 1 to 3 rows of 1 to 3 letters; a space is an empty cell. */
    shaped(this: void, spec: { pattern: string[]; keys: { [key: string]: ItemMatch }; result: ItemSpec }): void
        /** Adds a crafting recipe whose ingredients may go anywhere in the grid. */
    shapeless(this: void, spec: { items: ItemMatch[]; result: ItemSpec }): void
        /** Adds a furnace recipe; a furnace smelts a pack item only by one of these. */
    smelt(this: void, spec: { input: ItemMatch; result: ItemSpec }): void
}

/** An isolated world with its own players and tables, from `rooms.create` or `rooms.main`. */
interface Room {
        /** Takes the room away; players still in it keep the world. */
    destroy(): void
        /** This room's `world` table: its blocks, entities and displays. */
    message(text: Text, color?: Ink): void
        /** The room's number. */
    spawn_point: Vec3
}

/** A box of blocks: a `.schem` file from the pack, read once by `world.schematic`, or one a script wrote with `world.build`. `min` is the build's own lowest corner, which is the corner `origin` puts down; a file has no coordinates of its own, so its `min` is zero. */
interface Schematic {
        /** A new build flipped: "x" swaps east and west, "z" north and south. */
    mirror(axis: "x" | "z"): Schematic
        /** The build's width, height and length in blocks. */
    rotate(degrees: number): Schematic
}

/** A wall or floor of map frames showing a picture, from `world.screen`; it draws like a canvas and can answer clicks by pixel. */
interface Screen {
        /** Removes the screen. */
    destroy(): void
        /** Called with the pixel the player points at and the button, when a player clicks the screen. */
    on_click(this: void, arg0: ((this: void, player: Player, x: number, y: number, button: "left" | "right") => void) | false): unknown
        /** Returns this player's own layer over the screen; only they see it, and the shared picture shows where it is see-through. */
    view(player: Player): View
}

/** A purchase the player paid for, in Gems, that the pack has not handed over. */
interface ShopPurchase {
        /** The player's uuid. */
    player: string
        /** The product's key. */
    product: string
    request: string
}

/** One overrun, as `citadel.on_slow` is handed it. */
interface Slow {
        /** The short name of the hook that ran out: "on_tick", "every", or the event's own. */
    hook: string
        /** The pack's budget per tick, in milliseconds: `budget_ms` in citadel.yml. */
    of: number
        /** Callbacks not run for want of budget, since the script started. */
    skipped: number
        /** Milliseconds the pack spent in the tick that ran out. */
    used: number
}

/** A WebSocket a pack opened with `http.socket`. */
interface Socket {
        /** Closes the socket for good. */
    cancel(): void
        /** True while the connection is up. */
    send(text: string): boolean
}

/** One message of a socket. */
interface SocketMessage {
        /** The message as a table; an error when it is not JSON. */
    json(): any
        /** The message as text. */
    text: string
}

/** A sound `sound.stream` plays. Speakers are numbered from 1. */
interface SoundStream {
    add(at: SoundSpeaker): number
        /** Who hears it, changed while it plays. */
    listen(player: Player): void
        /** Speakers, for a sound made with `at`; on one with no place, an error. */
    move(speaker: number, at: SoundSpeaker): void
        /** False once stopped, or once a file that does not loop has played. */
    playing: boolean
    remove(speaker: number): void
    stop(): void
    unlisten(player: Player): void
}

/** One populate step of the overworld, as citadel.yml writes it, read from `game.terrain.steps`. */
interface TerrainStep {
        /** An ore step places its veins below this y. */
    below?: number
        /** Trees: one chunk in this many grows big trees instead of small ones. */
    big?: number
        /** The block a clay, ore or patch step places. */
    block?: string
        /** Trees: one chunk in this many gets one more tree. */
    bonus?: number
        /** Springs: the y is picked below this bound before `nesting` pushes it deeper. */
    bound?: number
        /** Patch: made one time in this many, in place of `count` times. */
    chance?: number
        /** How many tries, veins, blobs, clumps or springs the step makes in a chunk. */
    count?: number
        /** The fluid a springs step places: "water" or "lava". */
    fluid?: string
        /** Springs: how many times the y is picked again below itself; lava's 2 keeps it deeper than water's 1. */
    nesting?: number
        /** How long each clay blob or ore vein is. */
    size?: number
        /** Which populate step: "dungeons", "clay", "ore", "trees", "patch", "reeds", "cactus", "springs" or "snow". */
    step: string
}

/** Words wherever the API shows them: a string, or a table of runs. A table's entries are its runs in order (each a string or another table), and its named fields are the style of all of them; a run that names its own style keeps it. See "text" in docs/luau-api.md. */
interface TextRuns {
        /** Bold for every run that does not say otherwise. */
    bold?: boolean
        /** The colour of every run that does not pick its own: a colour value, a name or hex. */
    color?: Ink
        /** Called for every letter, every frame the text is on screen: hands back how that letter looks, or nil to leave it. */
    effect?: Effect
        /** Italic for every run that does not say otherwise. */
    italic?: boolean
        /** Struck through for every run that does not say otherwise. */
    strike?: boolean
        /** Underlined for every run that does not say otherwise. */
    underline?: boolean
}

/** A picture drawn in code: `game.texture(w, h)`. Where a texture is taken, a string is a PNG file in the pack instead. */
interface Texture {
        /** Returns a copy to draw on. */
    copy(): Texture
        /** Draws another texture over this one; its see-through pixels are skipped. */
    draw(other: Texture, x?: number, y?: number): void
        /** Paints every pixel one colour. */
    fill(color: Ink): void
        /** Draws a box's outline, one pixel wide. */
    frame(x: number, y: number, w: number, h: number, color: Ink): void
        /** Height in pixels. */
    height: number
        /** Paints each pixel in the area one of the colours at random, as for stone, bark or grain. */
    noise(x: number, y: number, w: number, h: number, colors: Ink[], seed?: number): void
        /** Sets one pixel; (0, 0) is the top left. */
    pixel(x: number, y: number, color: Ink): void
        /** Fills a rectangle of pixels. */
    rect(x: number, y: number, w: number, h: number, color: Ink): void
        /** Draws pixel art from rows of characters, each character painted with its ink, as on a screen. */
    sprite(x: number, y: number, rows: string[], inks: { [key: string]: Ink }, scale?: number): void
        /** Width in pixels. */
    width: number
}

/** What `on_think` gets: `n` bodies, and one buffer for each column with one f64 per body (entry i at byte i * 8). A yes or no is 1 or 0, an id of nothing is 0. Write the last nine to change them; a value left as it was changes nothing. [no documented members: opaque] */
interface Think {
}

/** A field easing over time, from tween or camera.path. [no documented members: opaque] */
interface Tween {
}

/** A raw RGB video playing on a picture, from `picture:play`; read `playing` or call `stop`. */
interface Video {
        /** False once it ends (and does not loop) or is stopped. */
    stop(): void
}

/** One player's own layer over a screen or canvas, from `screen:view(player)`; only they see it, drawn with the same calls. */
interface View {
        /** Removes this player's view; they see the shared picture again. */
    destroy(): void
}

/** A box of blocks that knows who is in it, checked once a tick. */
interface Zone {
        /** Returns true when the player is in the zone. */
    contains(player: Player): boolean
        /** Removes the zone. */
    destroy(): void
        /** Returns who is in the zone now. */
    players(): Player[]
}

// ============================== Type aliases ==============================
/** BarColor — from the documented typedef. */
type BarColor = "pink" | "blue" | "red" | "green" | "yellow" | "purple" | "white";

/** Billboard — from the documented typedef. */
type Billboard = "fixed" | "vertical" | "horizontal" | "center";

/** BlockPick — from the documented typedef. */
type BlockPick = string | { [key: number]: string; by?: Field | number };

/** BlockRef — from the documented typedef. */
type BlockRef = string | BlockDef;

/** Body — from the documented typedef. */
type Body = { id: number; kind: "player" | "mob" | "item" | "other" };

/** BodyRotation — from the documented typedef. */
type BodyRotation = { yaw?: number; pitch?: number };

/** BrowseEntry — from the documented typedef. */
type BrowseEntry = { id: string; name?: string; category?: string; motd?: string; icon?: string; players?: number; maxPlayers?: number; state?: string; region?: string };

/** Camera — from the documented typedef. */
type Camera = FixedCamera | EntityCamera | FreeCamera | OrbitCamera | ChaseCamera;

/** ColorName — from the documented typedef. */
type ColorName = "black" | "dark_blue" | "dark_green" | "dark_aqua" | "dark_red" | "dark_purple" | "gold" | "gray" | "dark_gray" | "blue" | "green" | "aqua" | "red" | "light_purple" | "yellow" | "white" | "orange" | "lime" | "cyan" | "purple" | "magenta" | "pink" | "transparent";

/** Context — from the documented typedef. */
type Context = "none" | "frame" | "menu" | "dropped" | "worn" | "held" | "own_hand";

/** DialogNode — from the documented typedef. */
type DialogNode = { [K in any]: any };

/** Drops — from the documented typedef. */
type Drops = "none" | "table" | ItemTable[];

/** Easing — from the documented typedef. */
type Easing = "linear" | "in" | "out" | "in_out" | "bounce";

/** Effect — from the documented typedef. */
type Effect = (this: void, letter: string, i: number, n: number, t: number) => LetterStyle | undefined;

/** EntityAmendOptions — from the documented typedef. */
type EntityAmendOptions = { priority?: number; replace?: boolean };

/** EntityDef — from the documented typedef. */
type EntityDef = { name: string; mob: false };

/** Face — from the documented typedef. */
type Face = "up" | "down" | "north" | "south" | "west" | "east";

/** Facing — from the documented typedef. */
type Facing = "north" | "south" | "west" | "east";

/** Feature — from the documented typedef. */
type Feature = "bossbar" | "potion_color" | "floor_frame" | "light" | "hex_color" | "glow_frame" | "display" | "hitbox" | "model" | "layout" | "dialog" | "overlay" | "resource_pack";

/** FluidRule — from the documented typedef. */
type FluidRule = { block: string; below: number; biome?: string; when?: Field | number };

/** GroundItem — from the documented typedef. */
type GroundItem = { id: number; item: string; count: number; at: Vec3 };

/** GroundRule — from the documented typedef. */
type GroundRule = { block: BlockPick; biome?: string; when?: Field | number; depth?: number };

/** HeadSkin — from the documented typedef. */
type HeadSkin = string | { value: string; signature?: string };

/** Ink — from the documented typedef. */
type Ink = Color | ColorName | string;

/** InventorySlot — from the documented typedef. */
type InventorySlot = { item: string; count: number; id?: string; damage?: number };

/** Item — from the documented typedef. */
type Item = { name: string; stack_size: number };

/** ItemMatch — from the documented typedef. */
type ItemMatch = string | { id?: string; item?: string };

/** ItemSpec — from the documented typedef. */
type ItemSpec = string | ItemTable;

/** ItemTable — from the documented typedef. */
type ItemTable = ItemMeta & { item: string } | ItemMeta & { canvas: Canvas };

/** Layout — from the documented typedef. */
type Layout = { _layout: true };

/** LayoutAlign — from the documented typedef. */
type LayoutAlign = "start" | "center" | "end";

/** LayoutNode — from the documented typedef. */
type LayoutNode = { _layout_node: true };

/** LetterStyle — from the documented typedef. */
type LetterStyle = { color?: Ink; bold?: boolean; italic?: boolean; underline?: boolean; strike?: boolean; text?: string };

/** LightSource — from the documented typedef. */
type LightSource = { at: Vec3; level?: number };

/** Looks — from the documented typedef. */
type Looks = string | { entity: string; block: string } | { entity: string; item: string };

/** ModelSkin — from the documented typedef. */
type ModelSkin = ModelMaterial | ModelTexture;

/** MountTarget — from the documented typedef. */
type MountTarget = EntityHandle | Npc | Display | ModelDisplay | Hitbox | Puppet;

/** NpcPose — from the documented typedef. */
type NpcPose = "standing" | "crouching" | "sleeping" | "swimming";

/** Occupant — from the documented typedef. */
type Occupant = Player | Npc | EntityHandle;

/** Orientation — from the documented typedef. */
type Orientation = Rotation | { forward: Vec3; up: Vec3 };

/** Persist — from the documented typedef. */
type Persist = "save" | "despawn";

/** Physics — from the documented typedef. */
type Physics = "vehicle" | "living" | "falling" | "item" | "none";

/** RayHit — from the documented typedef. */
type RayHit = { block: Vec3; face: Face };

/** Rotation — from the documented typedef. */
type Rotation = BodyRotation & { roll?: number };

/** Rules — from the documented typedef. */
type Rules = { survival: boolean; fall: boolean; damage: boolean; hunger: boolean; anticheat: boolean; day_cycle: boolean; redstone: boolean };

/** ScreenFacing — from the documented typedef. */
type ScreenFacing = "north" | "south" | "west" | "east" | "up";

/** SoundSpeaker — from the documented typedef. */
type SoundSpeaker = Vec3 | Player | EntityHandle;

/** Suggester — from the documented typedef. */
type Suggester = (this: void, player: Player, typed: string, args: { [key: string]: any }) => Suggestion[];

/** Suggestion — from the documented typedef. */
type Suggestion = string | { text: string; tooltip?: string };

/** Text — from the documented typedef. */
type Text = string | TextRuns | ((this: void, t: number) => any);

/** TextureRef — from the documented typedef. */
type TextureRef = Texture | string;

/** ThingGrid — from the documented typedef. */
type ThingGrid = { [key: number]: ThingRule; cell?: number; seed?: number };

/** ThingRule — from the documented typedef. */
type ThingRule = { shapes: Schematic[]; chance?: Field | number; biome?: string; when?: Field | number; afloat?: boolean; place?: "top" | "floor" | "ceiling"; y?: number[] };

/** Trigger — from the documented typedef. */
type Trigger = "ignite" | "explosion" | "fire";

/** Used — from the documented typedef. */
type Used = "used" | "pass";

/** WorldTarget — from the documented typedef. */
type WorldTarget = Player | MountTarget;

/** Worn — from the documented typedef. */
type Worn = { head?: ItemSpec; chest?: ItemSpec; legs?: ItemSpec; feet?: ItemSpec };

