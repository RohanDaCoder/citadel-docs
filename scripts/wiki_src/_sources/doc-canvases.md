# SOURCE: Canvases

- a frame display, by map id;
- a hand: a hotbar slot with `canvas = c`;
- a screen, after `screen:draw(c)`.
  An item display shows a blank map.
- Several walls can show one canvas.
- Drawing another canvas switches a wall’s picture. Only changed pixels are
  sent.
- A canvas draws like a screen. Changes go to the whole room once per tick.
  Later joiners get the whole picture.
- A destroyed canvas keeps its last picture on clients that saw it. Its id
  is never reused.

```luau
local c = world.canvas{}              -- one map; world.canvas{ width = 4, height = 2 } is 4 by 2 maps (16 at most a side)
c.id                                  -- the map id of its top-left map, for a filled_map
c.width, c.height                     -- pixels: 128, 128 (512, 256 for 4 by 2)
c:part(col, row)                      -- another of its maps, { id = .. }, from (0, 0) top-left
c:clear(color) c:set(x, y, color) c:fill(x, y, w, h, color)
c:rect(x, y, w, h, color, radius) c:circle(x, y, r, color)
c:text(x, y, "A♠", color, size) c:measure("A♠", size)
c:line(x0, y0, x1, y1, color, width) c:ring(x, y, r, color, width)
c:polygon(points, color) c:gradient(x, y, w, h, from, to, "across") c:sprite(x, y, rows, inks, scale)
c:pixels(x, y, w, h, data) c:draw(other, x, y) c:play{ file = "video/clip.rgb", fps = 20 }
c:view(player)                        -- that player's own layer over it; see screens
c:destroy()
```

## Video

`play` shows a video on a screen or canvas, with no script per frame. The
pack file holds raw RGB frames at the picture’s size. Make it with ffmpeg:

```sh
# a 4 by 2 screen is 512 x 256 pixels
ffmpeg -i clip.mp4 -vf "scale=512:256,fps=20" -f rawvideo -pix_fmt rgb24 mypack/video/clip.rgb
```

- Each frame snaps to the map palette. Only changed pixels are sent.
- A pixel changes at once when one of its channels moved more than 32 of 255
  from what the screen shows. A smaller move, of more than 8, waits for the
  next half second. So movement is as smooth as the video, and the noise of
  a camera is not sent in every frame.
- A fully changed frame costs 16 KB per map per player in the room. A 2 by 2
  screen at 10 fps is about 640 KB/s per player.
- Keep videos small or slow where many players watch.
- A video ends with the script.
- The file streams; it is never loaded whole.
- A **named pipe** in place of the file is a live picture. Another program
  writes the frames into it while the video plays, and the screen shows each
  frame at `fps`. A stream gives frames in bursts, so up to 24 frames wait in
  a queue; with more, the oldest are dropped. It has no end and does not
  loop: with no writer the picture stays, and a new writer continues it.
  `mkfifo mypack/video/live.rgb
ffmpeg -i https://example.org/live.flv -an -vf "fps=10,scale=512:256" -f rawvideo -pix_fmt rgb24 -y mypack/video/live.rgb
`

### Stream and sound

`url` plays a live FLV stream (H.264 video, AAC sound) with no other program.
On a screen, the stream’s sound is heard too.
`url` can also be an MP3 stream, as a radio station sends it (Icecast,
Shoutcast). It has sound only: the screen keeps the picture the pack draws on
it, so a radio’s own buttons and titles stay. The first bytes of the stream
say which kind it is.
A sound with no screen, from several speakers or from no place, is
[sound.stream](#sound).

- Players hear the sound through Simple Voice Chat: Citadel is a voice
  server for it, as a Paper server with the mod’s plugin is (UDP port
  24454, `CITADEL_VOICE_PORT`). A player without the mod sees the picture
  only.
- A locational sound comes from the screen’s centre and reaches the players
  within `distance`, fading out towards it. A static sound reaches everyone
  in the room, with no place and no fade.
- Sound needs a screen. A canvas has no place in the world, so
  `c:play{ url = .., audio = true }` is an error. A file of frames has no
  sound.
- The sound keeps time with the picture. If the server falls more than half
  a second behind, the sound skips to now and is not played late.
- A client older than 1.13 hears nothing.
- The sound stops with the video, or when the screen is destroyed.
