"use client";

import { useEffect, useMemo, useState } from "react";
import { useTheme } from "next-themes";
import { Search, Menu, X, Sun, Moon, ExternalLink, Home, AlertCircle } from "lucide-react";
import { useHashRoute, type Route } from "@/lib/docs/router";
import { loadPage, type AnyPage, type TocEntry } from "@/lib/docs/loader";
import { Sidebar } from "./Sidebar";
import { SearchDialog } from "./SearchDialog";
import { HomePage } from "./HomePage";
import { ArticlePage } from "./ArticlePage";
import { RefIndexPage } from "./RefIndexPage";
import { RefPage } from "./RefPage";
import { RefMemberPage } from "./RefMemberPage";
import { Toc } from "./Toc";

function ThemeToggle() {
  const { setTheme } = useTheme();
  return (
    <button
      aria-label="Toggle theme"
      onClick={() => {
        const isDark = document.documentElement.classList.contains("dark");
        setTheme(isDark ? "light" : "dark");
      }}
      className="flex size-8 items-center justify-center rounded-lg text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-700 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
    >
      <Sun className="hidden size-4 dark:block" />
      <Moon className="size-4 dark:hidden" />
    </button>
  );
}

export function DocsApp() {
  const { route } = useHashRoute();
  const [state, setState] = useState<{
    key: string;
    page: AnyPage | null;
    error: string | null;
  }>({ key: "", page: null, error: null });
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  const routeKey = JSON.stringify(route);
  const loading = state.key !== routeKey;

  useEffect(() => {
    let cancelled = false;
    if (route.kind === "home" || route.kind === "reference") {
      Promise.resolve().then(() => {
        if (!cancelled) setState({ key: routeKey, page: null, error: null });
      });
    } else {
      loadPage(route).then((data) => {
        if (cancelled) return;
        const label =
          route.kind === "guide"
            ? `Guide “${route.slug}”`
            : route.kind === "doc"
              ? `Page “${route.slug}”`
              : route.kind === "ref"
                ? `Reference “${route.name}”`
                : `${route.name}.${route.member}`;
        setState({ key: routeKey, page: data, error: data ? null : label });
      });
    }
    return () => {
      cancelled = true;
    };
  }, [route, routeKey]);

  const page = state.page;
  const notFound = state.error;

  const toc: TocEntry[] = useMemo(() => {
    if (!page) return [];
    if (page.type === "guide" || page.type === "doc") return page.toc;
    return [];
  }, [page]);

  const content = (() => {
    if (route.kind === "home") {
      return <HomePage onSearch={() => setSearchOpen(true)} />;
    }
    if (route.kind === "reference") {
      return <RefIndexPage onSearch={() => setSearchOpen(true)} />;
    }
    if (loading) {
      return (
        <div className="mx-auto max-w-[760px] animate-pulse px-5 py-12 sm:px-8">
          <div className="h-4 w-40 rounded bg-zinc-100 dark:bg-zinc-800" />
          <div className="mt-6 h-10 w-2/3 rounded bg-zinc-100 dark:bg-zinc-800" />
          <div className="mt-8 space-y-3">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="h-3.5 rounded bg-zinc-100 dark:bg-zinc-800" style={{ width: `${90 - i * 7}%` }} />
            ))}
          </div>
          <div className="mt-8 h-40 rounded-xl bg-zinc-100 dark:bg-zinc-800" />
        </div>
      );
    }
    if (notFound) {
      return (
        <div className="mx-auto max-w-lg px-5 py-24 text-center">
          <AlertCircle className="mx-auto size-10 text-zinc-300 dark:text-zinc-600" />
          <h1 className="mt-4 text-2xl font-bold text-zinc-900 dark:text-zinc-50">Not found</h1>
          <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
            {notFound} does not exist in this snapshot of the docs.
          </p>
          <a
            href="#/"
            onClick={(e) => {
              e.preventDefault();
              window.location.hash = "#/";
              window.scrollTo({ top: 0 });
            }}
            className="mt-6 inline-flex items-center gap-1.5 rounded-lg bg-amber-500 px-4 py-2 text-sm font-medium text-white shadow-sm transition-colors hover:bg-amber-600"
          >
            <Home className="size-4" />
            Back to overview
          </a>
        </div>
      );
    }
    if (!page) return null;
    switch (page.type) {
      case "guide":
      case "doc":
        return <ArticlePage data={page} route={route} />;
      case "ref":
        return <RefPage data={page} />;
      case "refmember":
        return <RefMemberPage data={page} />;
      default:
        return null;
    }
  })();

  return (
    <div className="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-zinc-200 bg-white/90 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/90">
        <div className="flex h-14 items-center gap-3 px-4 sm:px-6">
          <button
            aria-label="Open navigation"
            className="flex size-8 items-center justify-center rounded-lg text-zinc-500 transition-colors hover:bg-zinc-100 lg:hidden dark:text-zinc-400 dark:hover:bg-zinc-800"
            onClick={() => setMobileNavOpen(true)}
          >
            <Menu className="size-4.5" />
          </button>
          <a
            href="#/"
            onClick={(e) => {
              e.preventDefault();
              window.location.hash = "#/";
              window.scrollTo({ top: 0 });
            }}
            className="flex items-center gap-2.5"
          >
            <span className="flex size-7 items-center justify-center rounded-lg bg-gradient-to-br from-amber-400 to-amber-600 font-mono text-sm font-black text-white shadow-sm shadow-amber-500/30">
              C
            </span>
            <span className="text-[15px] font-semibold tracking-tight">Citadel Docs</span>
            <span className="hidden rounded-full border border-zinc-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider text-zinc-400 sm:inline dark:border-zinc-700 dark:text-zinc-500">
              v0.1.0
            </span>
          </a>
          <button
            onClick={() => setSearchOpen(true)}
            className="ml-auto flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-1.5 text-[13px] text-zinc-400 transition-colors hover:border-zinc-300 hover:text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:border-zinc-600 dark:hover:text-zinc-300"
          >
            <Search className="size-3.5" />
            <span className="hidden sm:inline">Search docs…</span>
            <kbd className="hidden rounded border border-zinc-200 bg-white px-1.5 py-0.5 font-mono text-[10px] dark:border-zinc-700 dark:bg-zinc-800 sm:inline">
              ⌘K
            </kbd>
          </button>
          <ThemeToggle />
          <a
            href="https://minefort.com/docs/citadel"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden items-center gap-1 rounded-lg px-2 py-1.5 text-[13px] text-zinc-400 transition-colors hover:text-zinc-700 md:flex dark:text-zinc-500 dark:hover:text-zinc-200"
            title="Official Minefort Citadel docs"
          >
            Official
            <ExternalLink className="size-3" />
          </a>
        </div>
      </header>

      <div className="flex">
        {/* Desktop sidebar */}
        <aside className="sticky top-14 hidden h-[calc(100vh-56px)] w-64 shrink-0 overflow-y-auto border-r border-zinc-200 px-4 py-6 lg:block dark:border-zinc-800">
          <Sidebar route={route} />
        </aside>

        {/* Mobile drawer */}
        {mobileNavOpen && (
          <div className="fixed inset-0 z-50 lg:hidden">
            <div
              className="absolute inset-0 bg-zinc-950/50 backdrop-blur-sm"
              onClick={() => setMobileNavOpen(false)}
            />
            <div className="absolute inset-y-0 left-0 w-72 overflow-y-auto border-r border-zinc-200 bg-white px-4 py-4 dark:border-zinc-800 dark:bg-zinc-950">
              <div className="mb-4 flex items-center justify-between">
                <span className="text-sm font-semibold">Navigation</span>
                <button
                  aria-label="Close navigation"
                  onClick={() => setMobileNavOpen(false)}
                  className="flex size-8 items-center justify-center rounded-lg text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                >
                  <X className="size-4" />
                </button>
              </div>
              <Sidebar route={route} onNavigate={() => setMobileNavOpen(false)} />
            </div>
          </div>
        )}

        {/* Content + TOC */}
        <div className="min-w-0 flex-1">
          <div className="mx-auto flex max-w-[1180px] justify-center">
            <main className="min-w-0 flex-1">{content}</main>
            <div className="pr-6">
              <Toc toc={toc} />
            </div>
          </div>
        </div>
      </div>

      <SearchDialog open={searchOpen} onOpenChange={setSearchOpen} />
    </div>
  );
}
