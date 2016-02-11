INSERT INTO ppiCVfolds ( corpus,
	parsertype,
	parser,
	kernel,
	c_preset,
	j,
	lmax,
	lmin,
	k,
	match_,
	normalized,
	input_format,
	kernel_script,
	led ) 
SELECT DISTINCT corpus,
	parsertype,
	parser,
	kernel,
	case when 
	ppicvid in (select ppicvid from ppicv where 
	((kernel='SpT' and c not in (0.0625, 1, 16, 64, 512)) or kernel='kBSPS' ))
	then null
	else c end,
	j,
	lmax,
	lmin,
	k,
	match_,
	normalized,
	input_format,
	kernel_script,
	led from ppiCV where ppicvfoldsid is NULL;

update ppicv set ppicvfoldsid = pf.ppicvfoldsid
from ppicvfolds as pf 
where ppicv.ppicvfoldsid IS NULL and
	ppicv.corpus IS NOT DISTINCT FROM  pf.corpus and
	ppicv.parsertype IS NOT DISTINCT FROM  pf.parsertype and 
	ppicv.parser IS NOT DISTINCT FROM  pf.parser and 
	ppicv.kernel IS NOT DISTINCT FROM  pf.kernel and 
	(pf.c_preset is null or ppicv.c IS NOT DISTINCT FROM  pf.c_preset) and 
	ppicv.j IS NOT DISTINCT FROM  pf.j and 
	ppicv.lmax IS NOT DISTINCT FROM  pf.lmax and 
	ppicv.lmin IS NOT DISTINCT FROM  pf.lmin and 
	ppicv.k IS NOT DISTINCT FROM  pf.k and 
	ppicv.match_ IS NOT DISTINCT FROM  pf.match_ and 
	ppicv.normalized IS NOT DISTINCT FROM  pf.normalized and 
	ppicv.input_format IS NOT DISTINCT FROM  pf.input_format and 
	ppicv.kernel_script IS NOT DISTINCT FROM  pf.kernel_script and 
	ppicv.led IS NOT DISTINCT FROM  pf.led;

--delete from ppicvfolds where ppicvfoldsid in (select pf.ppicvfoldsid from ppicvfolds pf 
--left outer join ppicv p on pf.ppicvfoldsid = p.ppicvfoldsid group by pf.ppicvfoldsid having count(ppicvid)=0);