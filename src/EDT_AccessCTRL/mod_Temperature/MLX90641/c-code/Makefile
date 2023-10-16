.PHONY: clean all

all: main libmlx90641.so libmlx90641_i2c_devtree.so libi2c.so

clean:
	rm -f main *.o
	rm -f src/*.o
	rm -f *.so

main.o: main.c
	gcc -c -fpic -Wall -Werror -o main.o main.c

src/i2c.o: src/i2c.c
	gcc -c -fpic -Wall -Werror -o src/i2c.o src/i2c.c

src/MLX90641_I2C_Driver_devtree.o: src/MLX90641_I2C_Driver_devtree.c
	gcc -c -fpic -Wall -Werror -o src/MLX90641_I2C_Driver_devtree.o src/MLX90641_I2C_Driver_devtree.c

src/MLX90641_API.o: src/MLX90641_API.c
	gcc -c -fpic -Wall -Werror -o src/MLX90641_API.o -Iinc src/MLX90641_API.c


main: main.o src/MLX90641_I2C_Driver_devtree.o src/MLX90641_API.o src/i2c.o
	gcc -o main main.o src/MLX90641_I2C_Driver_devtree.o src/MLX90641_API.o src/i2c.o -lm

libmlx90641.so: src/MLX90641_API.o
	gcc -shared -o $@ $<

libmlx90641_i2c_devtree.so: src/MLX90641_I2C_Driver_devtree.o
	gcc -shared -o $@ $<

libi2c.so: src/i2c.o
	gcc -shared -o $@ $<
