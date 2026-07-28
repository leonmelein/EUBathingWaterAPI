export const addToLocalStorageArray = function (name: string, value: string) {
    let existingArray: string | null = localStorage.getItem(name)
    let data: string[] = existingArray ? JSON.parse(existingArray) : [];

    if (!data.includes(value)) {
        data.push(value);
        localStorage.setItem(name, JSON.stringify(data));
    }
}

export const isInLocalStorageArray = function(name: string, value: string) {
    let existingArray: string | null = localStorage.getItem(name)
    let data: string[] = existingArray ? JSON.parse(existingArray) : [];

    return data.includes(value);
}

export function isoCodeToFlagEmoji(isoCode: string) {
    const code = isoCode.substring(0, 2)
    const flagIsoCode = { uk: "gb" }[code] ?? code;

    return flagIsoCode
        .toUpperCase()
        .replace(/./g, (char) => String.fromCodePoint(127397 + char.charCodeAt(0)));
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

export const countryColorsByIso: Record<string, string> = {
    al: "#da291c",
    at: "#ed2939",
    be: "#b31b34",
    bg: "#00966e",
    cy: "#d57800",
    cz: "#11457e",
    de: "#000000",
    dk: "#c60c30",
    ee: "#4891d9",
    es: "#aa151b",
    fr: "#0055a4",
    fi: "#003580",
    gr: "#0d5eaf",
    hr: "#cf1020",
    hu: "#436f4d",
    ie: "#169b62",
    it: "#009246",
    lt: "#fdb913",
    lu: "#00a3e0",
    lv: "#9e3039",
    mt: "#cf142b",
    nl: "#b85c00",
    pl: "#dc143c",
    pt: "#046a38",
    ro: "#002b7f",
    se: "#006aa7",
    si: "#005da4",
    sk: "#0b4ea2",
    ch: "#d52b1e",
    uk: "#012169"
};
