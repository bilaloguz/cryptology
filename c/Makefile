# Makefile for Cryptology C Library

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude
LDFLAGS =

# Directories
SRC_DIR = src/classical/substitution/monoalphabetic
OBJ_DIR = build/obj
BIN_DIR = build/bin
LIB_DIR = build/lib
EXAMPLE_DIR = examples
TEST_DIR = tests

# Source files
SOURCES = $(SRC_DIR)/caesar.c \
          $(SRC_DIR)/rot13.c \
          $(SRC_DIR)/atbash.c \
          $(SRC_DIR)/keyword.c \
          $(SRC_DIR)/affine.c

OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Library
LIBRARY = $(LIB_DIR)/libcryptology.a

# Examples
EXAMPLES = $(BIN_DIR)/example $(BIN_DIR)/custom_alphabets

# Targets
.PHONY: all clean examples tests

all: $(LIBRARY) examples

# Create directories
$(OBJ_DIR) $(BIN_DIR) $(LIB_DIR):
	mkdir -p $@

# Compile source files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Create static library
$(LIBRARY): $(OBJECTS) | $(LIB_DIR)
	ar rcs $@ $^

# Build examples
examples: $(EXAMPLES)

$(BIN_DIR)/example: $(EXAMPLE_DIR)/example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology -o $@

$(BIN_DIR)/custom_alphabets: $(EXAMPLE_DIR)/custom_alphabets.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology -o $@

# Clean build artifacts
clean:
	rm -rf build

# Run example
run-example: $(BIN_DIR)/example
	./$(BIN_DIR)/example

run-custom: $(BIN_DIR)/custom_alphabets
	./$(BIN_DIR)/custom_alphabets

# Help
help:
	@echo "Cryptology C Library - Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build library and examples (default)"
	@echo "  examples     - Build example programs"
	@echo "  clean        - Remove build artifacts"
	@echo "  run-example  - Run the main example"
	@echo "  run-custom   - Run custom alphabets example"
	@echo "  help         - Show this help message"

