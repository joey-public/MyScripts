function love.load()
end

function love.keypressed(key)
  if key == 'j' then
    love.event.push('quit')
  end
end

function love.update(dt)
end

function love.draw()
  --draw(ss, tiles[i], (i)*ss_stats.tile_w, 0*ss_stats.tile_h)
  --print(g_tiles[0])
end
