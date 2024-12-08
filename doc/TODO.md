# TODO
- The closing vuelta derecha feet end too early. Possibly there is a step forward with left on count 8. Go test it!
- There should be an easier way to connect figures. For example, it's perfectly possible to get from pal medio into Cuban 
  basic because your left leg doesn't care that it has to close an extra unit of distance when closing anyway. Yet,
  Cuban basic expects feet together.
  Really, there is a "glue step" that could be generated on the fly in a sequence. We do exactly this in the `Loopable`
  function except there we use the end state of the *same* pattern rather than *any* pattern.
   - You could define some kind of glue inventory that says "you can connect this ending state to this starting state, although
     you need to replace the first count".
   - We've written about this before as having a "simulated base" and a "canonical base". You don't need to clarify that cruzado
     can start in crossed legs because that's what it ends in when you simulate it, but this might not suffice since there
     are actually *more than two* entry points.
- Smarter arrows:
  - Bendy arrows (can probably figure this out based on clockwise vs counterclockwise)
  - For figures like enchufla, there should be a difference between a clockwise and a counterclockwise half-turn.
  - Turns can be over 360°. The arrows should spiral then.
  - Disambiguation for leg crosses.
    - Imagine a grid `| L |  | R |`. Now it turns into `| R |  | L |`. How can we know the bend of the arrows that follow?
      Extra difficulty: if the person rotates 180°, their legs become untangled and they can do any move again.
- Centre-of-mass view (i.e. just leader-follower, not the feet)
  - You can do this quite easily, I believe. Rather than visualising the feet, visualise the point average between the feet,
    and perhaps connect them with lines. Boom.