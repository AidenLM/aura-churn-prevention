import Link from 'next/link';

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-[#F4F5F7]">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 lg:px-8 py-4 lg:py-5">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-[#5E6C84] hover:text-[#172B4D] transition-colors">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <div>
              <h1 className="text-[#172B4D] text-2xl font-bold">Raporlar</h1>
              <p className="text-[#5E6C84] text-sm">Analiz raporları ve istatistikler</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-8">
        <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm text-center">
          <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="text-[#172B4D] text-xl font-semibold mb-2">Raporlar</h2>
          <p className="text-[#5E6C84] text-sm mb-6">Bu sayfa yakında eklenecek</p>
          <Link href="/dashboard" className="inline-block px-6 py-3 rounded-lg bg-[#0052CC] hover:bg-[#0747A6] text-white text-sm font-medium transition-colors">
            Dashboard'a Dön
          </Link>
        </div>
      </main>
    </div>
  );
}
