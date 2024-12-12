local function calc_spritesheet_stats(ss, tileW, tileH)
  local ssW, ssH = ss:getWidth(), ss:getHeight()
  local ss_rows = math.floor(ssH, tileH)
  local ss_cols = math.floor(ssW, tileW)
  local n_tiles = math.floor(ss_rows*ss_cols)
  return {ss_w=ssW, ss_h=ssH, 
          tile_w=tileW, tile_h=tileH, 
          nrows=ss_rows, ncols=ss_cols, 
          ntiles=ss_rows*ss_cols}
end

local function load_tiles(ss, ss_stats)
  local tiles = {}
  for i=0, ss_stats.ntiles do
    table.insert(tiles, 'Hi!')
  end
  return tiles
end

local function load_quad(x, y, ss_stats)
  local s = ss_stats
  return love.graphics.newQuad(x, y, s.tile_w, s.tile_h, s.ss_w, s.ss_h) 
end

function love.load()
  local png_path = 'assets/roguelikeSheet_transparent.png'
  local ss = love.graphics.newImage(png_path)
  local tw, th = 16, 16
  g_spritesheet = ss
  g_spritesheet_stats = calc_spritesheet_stats(ss, tw, th)
  g_tiles = load_tiles(g_spritesheet, g_spritesheet_stats)
end

function love.keypressed(key)
  if key == 'j' then 
    love.event.push('quit')
  end
end

function love.update(dt)
end

function love.draw() 
  local print = love.graphics.print
  local draw = love.graphics.draw
  --draw(ss, tiles[i], (i)*ss_stats.tile_w, 0*ss_stats.tile_h)
  --print(g_tiles[0])
end
