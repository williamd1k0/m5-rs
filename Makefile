
all: configs flags

configs: configs.h
configs.h: configs.h.in
	@cp $< $@

flags: compile_flags.txt
compile_flags.txt: compile_flags.txt.in
	@sed "s|{HOME}|${HOME}|g" $< | tee $@

.PHONY: all configs flags
