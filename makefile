block_sort:
	@gcc ordenacao/block_sort.c -o block_sort
	@./block_sort $(FILE_PATH) $(SIZE_ARR) $(BLOCK_SIZE) $(SHOW_VECTOR_RESULT) $(QTD_TESTES)

radix_sort:
	@gcc ordenacao/radix_sort.c -o radix_sort
	@./radix_sort $(FILE_PATH) $(SIZE_ARR) $(SHOW_VECTOR_RESULT) $(QTD_TESTES)