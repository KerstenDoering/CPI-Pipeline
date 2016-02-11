create or replace function r (double precision) returns numeric as 'select round(cast(100*$1 as numeric),1);' 
language SQL immutable returns null on null input;

drop table if exists ppiCVoutput;
drop table if exists ppiCV cascade;
drop table if exists ppiCVfolds;

CREATE TABLE ppiCVfolds(
	ppiCVfoldsid serial PRIMARY KEY,
	corpus text, -- REFERENCES corpus,
	parsertype text,
	parser text,
	kernel text,
	kernel_script text,
	led text,
	c_preset double precision,
	j double precision,
	lmax integer,
	lmin integer,
	k integer,
	match_ text,
	normalized boolean,
	input_format text
);

CREATE UNIQUE INDEX unique_CVfolds_idx on ppiCVfolds(
coalesce(corpus,'*** NULLLLLL ***'),
coalesce(parsertype,'*** NULLLLLL ***'),
coalesce(parser,'*** NULLLLLL ***'),
coalesce(kernel,'*** NULLLLLL ***'),
coalesce(kernel_script,'*** NULLLLLL ***'),
coalesce(c_preset,-1),
coalesce(j,-1),
coalesce(lmax,-1),
coalesce(lmin,-1),
coalesce(k,-1),
coalesce(led,'*** NULLLLLL ***'),
coalesce(normalized,'0'),
coalesce(match_,'*** NULLLLLL ***'),
coalesce(input_format,'*** NULLLLLL ***'));


CREATE TABLE ppiCV ( ppiCVid serial NOT NULL,
	ppiCVfoldsid integer REFERENCES ppiCVfolds on delete cascade,
	corpus text, -- REFERENCES corpus,
	parsertype text,
	parser text,
	kernel text,
	kernel_script text,
	led text,
	c double precision,
	j double precision,
	lmax integer,
	lmin integer,
	k integer,
	match_ text,
	fold integer,
	normalized boolean,
	input_format text,
	tp integer check(tp>=0 OR tp is NULL),
	fn integer check(fn>=0 OR fn is NULL),
	tn integer check(tn>=0 OR tn is NULL),
	fp integer check(fp>=0 OR fp is NULL),
	total integer check(total>=0 OR total is NULL),
	auc double precision check(auc>=0 OR auc is NULL),
	precision_ double precision check(precision_>=0 OR precision_ is NULL),
	recall double precision check(recall>=0 OR recall is NULL),
	f_measure double precision check(f_measure>=0 OR f_measure is NULL),
	learn_sec double precision check(learn_sec>=0 OR learn_sec is NULL),
	classify_sec double precision check(classify_sec>=0 OR classify_sec is NULL),
	sv_num integer check(sv_num>0 OR sv_num is NULL),
	forced_threshold double precision,
	CONSTRAINT ppiCV_pkey PRIMARY KEY (ppiCVid),
	CONSTRAINT unique_CVexperiment UNIQUE (corpus,parsertype,parser,kernel,kernel_script,c,j,lmax,lmin,k,fold,led,normalized,match_,input_format));

CREATE UNIQUE INDEX unique_CVexperiment_idx on ppiCV(
coalesce(corpus,'*** NULLLLLL ***'),
coalesce(parsertype,'*** NULLLLLL ***'),
coalesce(parser,'*** NULLLLLL ***'),
coalesce(kernel,'*** NULLLLLL ***'),
coalesce(kernel_script,'*** NULLLLLL ***'),
coalesce(case when (kernel <> 'SpT' or (kernel = 'SpT' and c in (0.0625, 1, 16, 64, 512))) 
	and ppiCV.kernel <> 'kBSPS' then c else -1 end,-1),
coalesce(j,-1),
coalesce(lmax,-1),
coalesce(lmin,-1),
coalesce(k,-1),
coalesce(fold,-1),
coalesce(led,'*** NULLLLLL ***'),
coalesce(normalized,'0'),
coalesce(match_,'*** NULLLLLL ***'),
coalesce(input_format,'*** NULLLLLL ***'));

create index ppicvfolds_on_ppicv on ppicv (ppicvfoldsid) where ppicvfoldsid is not null;


drop view if exists foldCVcombined;
drop view if exists foldCV;
drop view if exists foldCVspec;

CREATE OR REPLACE VIEW foldCV AS 
SELECT ppiCV.ppicvfoldsid,
	ppiCV.corpus,
	ppiCV.parsertype,
	ppiCV.parser,
	ppiCV.kernel,
	ppiCV.c,
	ppiCV.j,
	ppiCV.lmax,
	ppiCV.lmin,
	ppiCV.k,
	ppiCV.match_,
	ppiCV.normalized,
	ppiCV.input_format,
	ppiCV.kernel_script,
	ppiCV.led,
	avg(ppiCV.auc) AS auc,
	avg(ppiCV.precision_) AS precision_,
	avg(ppiCV.recall) AS recall,
	avg(ppiCV.f_measure) AS f_measure,
	avg(ppiCV.learn_sec) AS learn_sec,
	avg(ppiCV.classify_sec) AS classify_sec,
	avg(ppiCV.sv_num) AS sv_num,
	count(ppiCV.ppiCVid) AS cnt
	FROM ppiCV where
	(ppiCV.kernel <> 'SpT' or (ppicv.kernel = 'SpT' and ppiCV.c in (0.0625, 1, 16, 64, 512))) 
	and ppiCV.kernel <> 'kBSPS'
	GROUP BY 
	ppiCV.ppicvfoldsid,
	ppiCV.corpus,
	ppiCV.parsertype,
	ppiCV.parser,
	ppiCV.kernel,
	ppiCV.c,
	ppiCV.j,
	ppiCV.lmax,
	ppiCV.lmin,
	ppiCV.k,
	ppiCV.match_,
	ppiCV.normalized,
	ppiCV.input_format,
	ppiCV.kernel_script,
	ppiCV.led ORDER BY ppiCV.corpus,
	avg(ppiCV.auc) DESC,
	ppiCV.j,
	ppiCV.kernel_script;

CREATE OR REPLACE VIEW foldCVspec AS 
SELECT ppiCV.ppicvfoldsid,
	ppiCV.corpus,
	ppiCV.parsertype,
	ppiCV.parser,
	ppiCV.kernel,
	avg(ppiCV.c) as c,
	ppiCV.j,
	ppiCV.lmax,
	ppiCV.lmin,
	ppiCV.k,
	ppiCV.match_,
	ppiCV.normalized,
	ppiCV.input_format,
	ppiCV.kernel_script,
	ppiCV.led,
	avg(ppiCV.auc) AS auc,
	avg(ppiCV.precision_) AS precision_,
	avg(ppiCV.recall) AS recall,
	avg(ppiCV.f_measure) AS f_measure,
	avg(ppiCV.learn_sec) AS learn_sec,
	avg(ppiCV.classify_sec) AS classify_sec,
	avg(ppiCV.sv_num) AS sv_num,
	count(ppiCV.ppiCVid) AS cnt
	FROM ppiCV where 
	((ppiCV.kernel='SpT' and ppiCV.c not in (0.0625, 1, 16, 64, 512)) or ppiCV.kernel='kBSPS' )
	GROUP BY  ppiCV.ppicvfoldsid,
	ppiCV.corpus,
	ppiCV.parsertype,
	ppiCV.parser,
	ppiCV.kernel,
	ppiCV.j,
	ppiCV.lmax,
	ppiCV.lmin,
	ppiCV.k,
	ppiCV.match_,
	ppiCV.normalized,
	ppiCV.input_format,
	ppiCV.kernel_script,
	ppiCV.led ORDER BY ppiCV.corpus,
	avg(ppiCV.auc) DESC,
	ppiCV.j,
	ppiCV.kernel_script;


CREATE OR REPLACE VIEW foldCVcombined as 
SELECT ppicvfoldsid,
	corpus,
	parsertype,
	parser,
	kernel,
	c_normal,
	c_spec,
	j,
	lmax,
	lmin,
	k,
	match_,
	normalized,
	input_format,
	kernel_script,
	led,
	auc,
	precision_,
	recall,
	f_measure,
	learn_sec,
	classify_sec,
	sv_num,
	cnt
	FROM (select *,foldCV.c as c_normal,null as c_spec from foldCV
union
select *,null as c_normal,foldCVspec.c as c_spec from foldCVspec) as b
;

--
-- output of CV experiments
--
CREATE TABLE ppiCVoutput
(
  expId       integer NOT NULL  REFERENCES ppiCV(ppiCVid) on delete cascade,
  pair        text    NOT NULL, --  REFERENCES pair,
  output      boolean NOT NULL,
  prediction  float,
  PRIMARY KEY (expId, pair)
);

CREATE UNIQUE INDEX ppi_cv_output_idx
  ON ppiCVoutput (expId, output, pair);
