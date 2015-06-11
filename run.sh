# Yossof limits
python python/makeSMSplots.py config/SUS14006/yossof/T2cc/T2cc_SUS14006.cfg T2cc_yossof_

# Excess limits (unknown source, but early)
python python/makeSMSplots.py config/SUS14006/excess/T2cc/T2cc_SUS14006.cfg T2cc_excess_
python python/makeSMSplots.py config/SUS14006/excess/T2_4body/T2degen_SUS14006.cfg T2degen_excess_
python python/makeSMSplots.py config/SUS14006/excess/T2_4body_boosted/T2degen_SUS14006.cfg T2degen_boosted_excess_

# Toys limits (from Rob, unknown version, but recent)
python python/makeSMSplots.py config/SUS14006/toys/T2cc/T2cc_SUS14006.cfg T2cc_toys_
python python/makeSMSplots.py config/SUS14006/toys/T2_4body/T2degen_SUS14006.cfg T2degen_toys_

# Chris limits (30th Mar, asymptotic CLs)
python python/makeSMSplots.py config/SUS14006/chris/T2cc/T2cc_SUS14006.cfg T2cc_chris_asymp_
python python/makeSMSplots.py config/SUS14006/chris/T2_4body/T2degen_SUS14006.cfg T2degen_chris_asymp_

# Latest limits (these should be used for paper)
python python/makeSMSplots.py config/SUS14006/latest/T2cc/T2cc_SUS14006.cfg T2cc_latest_
python python/makeSMSplots.py config/SUS14006/latest/T2_4body/T2degen_SUS14006.cfg T2degen_latest_
