# Makefile for Cryptology C Library

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude
LDFLAGS = -lm

# Directories
MONOALPHABETIC_SRC_DIR = src/classical/substitution/monoalphabetic
POLYGRAPHIC_SRC_DIR = src/classical/substitution/polygraphic
FRACTIONATED_SRC_DIR = src/classical/substitution/fractionated
POLYALPHABETIC_SRC_DIR = src/classical/substitution/polyalphabetic
COMPOSITE_SRC_DIR = src/classical/substitution/composite
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
                     $(POLYGRAPHIC_SRC_DIR)/monoalphabetic_squares.c \
                     $(POLYGRAPHIC_SRC_DIR)/playfair.c \
                     $(POLYGRAPHIC_SRC_DIR)/two_square.c \
                     $(POLYGRAPHIC_SRC_DIR)/four_square.c \
                     $(POLYGRAPHIC_SRC_DIR)/hill.c

FRACTIONATED_SOURCES = $(FRACTIONATED_SRC_DIR)/bifid.c \
                      $(FRACTIONATED_SRC_DIR)/trifid.c

POLYALPHABETIC_SOURCES = $(POLYALPHABETIC_SRC_DIR)/alberti.c $(POLYALPHABETIC_SRC_DIR)/vigenere.c $(POLYALPHABETIC_SRC_DIR)/beaufort.c $(POLYALPHABETIC_SRC_DIR)/autokey.c $(POLYALPHABETIC_SRC_DIR)/chaocipher.c $(POLYALPHABETIC_SRC_DIR)/gronsfeld.c $(POLYALPHABETIC_SRC_DIR)/porta.c $(POLYALPHABETIC_SRC_DIR)/reihenschieber.c

COMPOSITE_SOURCES = $(COMPOSITE_SRC_DIR)/straddling_checkerboard.c $(COMPOSITE_SRC_DIR)/nihilist.c $(COMPOSITE_SRC_DIR)/adfgvx.c $(COMPOSITE_SRC_DIR)/vic.c

SOURCES = $(MONOALPHABETIC_SOURCES) $(POLYGRAPHIC_SOURCES) $(FRACTIONATED_SOURCES) $(POLYALPHABETIC_SOURCES) $(COMPOSITE_SOURCES)

MONOALPHABETIC_OBJECTS = $(MONOALPHABETIC_SOURCES:$(MONOALPHABETIC_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
POLYGRAPHIC_OBJECTS = $(POLYGRAPHIC_SOURCES:$(POLYGRAPHIC_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
FRACTIONATED_OBJECTS = $(FRACTIONATED_SOURCES:$(FRACTIONATED_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
POLYALPHABETIC_OBJECTS = $(POLYALPHABETIC_SOURCES:$(POLYALPHABETIC_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
COMPOSITE_OBJECTS = $(COMPOSITE_SOURCES:$(COMPOSITE_SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
OBJECTS = $(MONOALPHABETIC_OBJECTS) $(POLYGRAPHIC_OBJECTS) $(FRACTIONATED_OBJECTS) $(POLYALPHABETIC_OBJECTS) $(COMPOSITE_OBJECTS)

# Library
LIBRARY = $(LIB_DIR)/libcryptology.a

# Examples
EXAMPLES = $(BIN_DIR)/example $(BIN_DIR)/custom_alphabets $(BIN_DIR)/polygraphic_example $(BIN_DIR)/composable_ciphers $(BIN_DIR)/fractionated_example $(BIN_DIR)/alberti_example $(BIN_DIR)/vigenere_example $(BIN_DIR)/beaufort_example $(BIN_DIR)/autokey_example $(BIN_DIR)/chaocipher_example $(BIN_DIR)/gronsfeld_example $(BIN_DIR)/porta_example $(BIN_DIR)/reihenschieber_example $(BIN_DIR)/straddling_checkerboard_example $(BIN_DIR)/nihilist_example $(BIN_DIR)/adfgvx_example $(BIN_DIR)/vic_example $(BIN_DIR)/test_chaocipher

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

$(OBJ_DIR)/%.o: $(POLYALPHABETIC_SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR)/%.o: $(COMPOSITE_SRC_DIR)/%.c | $(OBJ_DIR)
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

$(BIN_DIR)/alberti_example: $(EXAMPLE_DIR)/alberti_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/vigenere_example: $(EXAMPLE_DIR)/vigenere_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/beaufort_example: $(EXAMPLE_DIR)/beaufort_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/autokey_example: $(EXAMPLE_DIR)/autokey_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/chaocipher_example: $(EXAMPLE_DIR)/chaocipher_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/gronsfeld_example: $(EXAMPLE_DIR)/gronsfeld_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/porta_example: $(EXAMPLE_DIR)/porta_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/reihenschieber_example: $(EXAMPLE_DIR)/reihenschieber_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/straddling_checkerboard_example: $(EXAMPLE_DIR)/straddling_checkerboard_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/nihilist_example: $(EXAMPLE_DIR)/nihilist_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/adfgvx_example: $(EXAMPLE_DIR)/adfgvx_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/vic_example: $(EXAMPLE_DIR)/vic_example.c $(LIBRARY) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -L$(LIB_DIR) -lcryptology $(LDFLAGS) -o $@

$(BIN_DIR)/test_chaocipher: test_chaocipher_simple.c $(LIBRARY) | $(BIN_DIR)
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

run-alberti: $(BIN_DIR)/alberti_example
	./$(BIN_DIR)/alberti_example

run-vigenere: $(BIN_DIR)/vigenere_example
	./$(BIN_DIR)/vigenere_example

run-beaufort: $(BIN_DIR)/beaufort_example
	./$(BIN_DIR)/beaufort_example

run-gronsfeld: $(BIN_DIR)/gronsfeld_example
	./$(BIN_DIR)/gronsfeld_example

run-porta: $(BIN_DIR)/porta_example
	./$(BIN_DIR)/porta_example

run-reihenschieber: $(BIN_DIR)/reihenschieber_example
	./$(BIN_DIR)/reihenschieber_example

run-straddling-checkerboard: $(BIN_DIR)/straddling_checkerboard_example
	./$(BIN_DIR)/straddling_checkerboard_example

run-test-chaocipher: $(BIN_DIR)/test_chaocipher
	./$(BIN_DIR)/test_chaocipher

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
	@echo "  run-alberti     - Run Alberti cipher example"
	@echo "  run-vigenere    - Run Vigenère cipher example"
	@echo "  run-beaufort    - Run Beaufort cipher example"
	@echo "  run-chaocipher   - Run Chaocipher cipher example"
	@echo "  run-gronsfeld    - Run Gronsfeld cipher example"
	@echo "  run-porta        - Run Porta cipher example"
	@echo "  run-reihenschieber - Run Reihenschieber cipher example"
	@echo "  run-straddling-checkerboard - Run Straddling Checkerboard cipher example"
	@echo "  help            - Show this help message"

