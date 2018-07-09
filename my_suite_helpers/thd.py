def thd(T1, T2):
    _sum = 0
    _thd = 0
    for k in range(0, len(T2)):
        add = float(T2.iloc[[k]]["num"])
        _sum += float(T2.iloc[[k]]["num"])
        _found = False
        for m in range(0, len(T1)):
            term1 = T2.iloc[[k]]["term"].tolist()[0]
            term2 = T1.iloc[[m]]["term"].tolist()[0]
            if str(T2.iloc[[k]]["term"].tolist()[0]) == str(T1.iloc[[m]]["term"].tolist()[0]):
                _thd += abs(float(T2.iloc[[k]]["num"].tolist()[0])-float(T1.iloc[[m]]["num"].tolist()[0]))
                _found = True
        if not _found:
            _thd += float(T2.iloc[[k]]["num"].tolist()[0])
    _thdr = _thd/_sum
    eps = _sum/2
    return _thd, _thdr, eps