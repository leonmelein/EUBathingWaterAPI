export const addToLocalStorageArray = function (name: string, value: string) {
    let existingArray: string | null = localStorage.getItem(name)
    let data = existingArray ? existingArray.split(',') : [];

    data.push(value);
    localStorage.setItem(name, data.toString())
}

export const countriesByIso:Record<string, string> = {
    al: "Albania",
    at: "Austria",
    be: "Belgium",
    bg: "Bulgaria",
    cy: "Cyprus",
    cz: "Czechia",
    de: "Germany",
    dk: "Denmark",
    ee: "Estonia",
    es: "Spain",
    fr: "France",
    fi: "Finland",
    gr: "Greece",
    hr: "Croatia",
    hu: "Hungary",
    ie: "Ireland",
    it: "Italy",
    lt: "Lithuania",
    lu: "Luxembourg",
    lv: "Latvia",
    mt: "Malta",
    nl: "Netherlands",
    pl: "Poland",
    pt: "Portugal",
    ro: "Romania",
    se: "Sweden",
    si: "Slovenia",
    sk: "Slovakia",
    ch: "Switzerland",
    uk: "United Kingdom"
};