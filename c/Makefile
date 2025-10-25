# Makefile for Cryptology C Library

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude
LDFLAGS = -lm

# Directories
MONOALPHABETIC_SRC_DIR = src/classical/substitution/monoalphabetic
POLYGRAPHIC_SRC_DIR = src/classical/substitution/polygraphic
FRACTIONATED_SRC_DIR = src/classical/substitution/fractionated
OBJ_DIR = build/obj
BIN_DIR = build/bin
LIB_DIR = build/lib
EXAMPLE_DIR = examples
TEST_DIR = tests

# Source files
MONOALPHABETIC_SOURCES = $(MONOALPHABETIC_SRC_DIR)/caesar.c \
                        $(MONOALPHABETIC_SRC_DIR)/rot13.c \
                        $(MONOALPHABETIC_SRC_DIR)/atbash.c \
                        $(MONOALPHABETIC_SRC_DIR)/keyword.c \
                        $(MONOALPHABETIC_SRC_DIR)/affine.c

POLYGRAPHIC_SOURCES = $(POLYGRAPHIC_SRC_DIR)/alphabet_utils.c \
                     $(POLYGRAPHIC_SRC_DIR)/playfair.c \
                     $(POLYGRAPHIC_SRC_DIR)/two_square.c \
                     $(POLYGRAPHIC_SRC_DIR)/four_square.c \
                     $(POLYGRAPHIC_SRC_DIR)/hill.c

FRACTIONATED_SOURCES = $(FRACTIONATED_SRC_DIR)/bifid.c \
                      $(FRACTIONATED_SRC_DIR)/trifid.c

SOURCES = $(MONOALPHABETIC_SOURCES) $(POLYGRAPHIC_SOURCES) $(FRACTIONATED_SOURCES)

MONOALPHABETIC_OBJECTS = $(MONOALPHABETIC_SOURCES:$(MONOALPHABETIC_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
POLYGRAPHIC_OBJECTS = $(POLYGRAPHIC_SOURCES:$(POLYGRAPHIC_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
FRACTIONATED_OBJECTS = $(FRACTIONATED_SOURCES:$(FRACTIONATED_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
OBJECTS = $(MONOALPHABETIC_OBJECTS) $(POLYGRAPHIC_OBJECTS) $(FRACTIONATED_OBJECTS)

# Library
LIBRARY = $(LIB_DIR)/libcryptology.a

# Examples
EXAMPLES = $(BIN_DIR)/example $(BIN_DIR)/custom_alphabets $(BIN_DIR)/polygraphic_example $(BIN_DIR)/composable_ciphers $(BIN_DIR)/fractionated_example

# Targets
.PHONY: all clean examples tests

all: $(LIBRARY) examples

# Create directories
$(OBJ_DIR) $(BIN_DIR) $(LIB_DIR):
	mkdir -p $@

# Compile source files
$(OBJ_DIR)/%.o: $(MONOALPHABETIC_SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR)/%.o: $(POLYGRAPHIC_SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR)/%.o: $(FRACTIONATED_SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Create static library
$(LIBRARY): $(OBJECTS) | $(LIB_DIR)
	ar rcs $@ $^

# Build examples
examples: $(EXAMPLES)

$(BIN_DIR)/example: $(EXAMPLE_DIR)/example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/custom_alphabets: $(EXAMPLE_DIR)/custom_alphabets.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/polygraphic_example: $(EXAMPLE_DIR)/polygraphic_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/composable_ciphers: $(EXAMPLE_DIR)/composable_ciphers.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/fractionated_example: $(EXAMPLE_DIR)/fractionated_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

# Clean build artifacts
clean:
	rm -rf build

# Run example
run-example: $(BIN_DIR)/example
	./$(BIN_DIR)/example

run-custom: $(BIN_DIR)/custom_alphabets
	./$(BIN_DIR)/custom_alphabets

run-polygraphic: $(BIN_DIR)/polygraphic_example
	./$(BIN_DIR)/polygraphic_example

run-composable: $(BIN_DIR)/composable_ciphers
	./$(BIN_DIR)/composable_ciphers

run-fractionated: $(BIN_DIR)/fractionated_example
	./$(BIN_DIR)/fractionated_example

# Help
help:
	@echo "Cryptology C Library - Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build library and examples (default)"
	@echo "  examples     - Build example programs"
	@echo "  clean        - Remove build artifacts"
	@echo "  run-example     - Run the main example"
	@echo "  run-custom      - Run custom alphabets example"
	@echo "  run-polygraphic - Run polygraphic ciphers example"
	@echo "  run-composable  - Run composable cipher system example"
	@echo "  run-fractionated - Run fractionated ciphers example"
	@echo "  help            - Show this help message"

