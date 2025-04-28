# anagrama_dinamico:
# 	@gcc programacao_dinamica/calcular_anagrama_dinamico.c -o anagrama_dinamico
# 	@./anagrama_dinamico $(FILE_PATH) $(QTD_WORD) $(QTD_TEST) $(SHOW_RESULT)

# anagrama_recursivo:
# 	@gcc programacao_dinamica/calcular_anagrama_recursivo.c -o anagrama_recursivo
# 	@./anagrama_recursivo $(FILE_PATH) $(QTD_WORD) $(QTD_TEST) $(SHOW_RESULT)


anagrama_dinamico:
	@python3 programacao_dinamica/calcular_anagrama_dinamico.py $(FILE_PATH) $(QTD_WORD) $(QTD_TEST) $(SHOW_RESULT)

anagrama_recursivo:
	@python3 programacao_dinamica/calcular_anagrama_recursivo.py $(FILE_PATH) $(QTD_WORD) $(QTD_TEST) $(SHOW_RESULT)