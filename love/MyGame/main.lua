function love.load()
    sprites = love.graphics.newImage('sprites.png')
end

function love.draw()
    love.graphics.print("Hello World", 400, 300)
    love.graphics.draw(sprites, 0, 0)
end


