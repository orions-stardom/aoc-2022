nnoremap gV 0P<c-v>`]I... <Esc>gv>gv:s/\s\+$//e<CR>:nohl<CR>

function! s:Advent(day) abort
	if !(a:day >= 1 && a:day <= 25)
		throw "Invalid day (".a:day.") must be between 1-25"
	endif

	let fname="day_".printf("%02d", a:day).".py"
	if filereadable(l:fname)
		exec "e ".l:fname
	else
		e template.py
		exec "saveas ".l:fname
		exec "H chmod +x ".l:fname
		exec "H clear"
		call TerminalClose()
	endif
endfunction	

command! -nargs=1 Advent :call s:Advent(<args>)
